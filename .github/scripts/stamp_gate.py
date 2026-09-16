"""Label a pull request `stamp-eligible` or `needs-human` from the repository's stamp policy, and
approve it when the policy allows.

Deterministic: every rule is a size, path, regex, label, author or review-presence check.
Reads the PR through the GitHub API only; never checks out or runs the PR's code. A fleet
floor of paths is refused in every repository before the policy is consulted, so no policy
can make an infrastructure, CI or container change eligible.

Env: GH_TOKEN, REPO (owner/name), PR_NUMBER (empty = reconcile every open PR), POLICY (path),
DEFAULT_BRANCH, POLICY_SHA (optional). DRY_RUN=1 prints the verdict and the writes it would
make without making any, and evaluates closed PRs. Exit 0 on any verdict; non-zero only when
the gate itself could not run, or when a reconcile failed on at least one PR.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field

import yaml

MARKER = "<!-- stamp-gate -->"
FLOOR_PATHS = (
    ".github/**",
    "infra/**",
    "infrastructure/**",
    "terraform/**",
    "**/*.tf",
    "**/*.tfvars",
    "**/*.hcl",
    "cloudbuild*.yaml",
    "cloudbuild*.yml",
    "**/Dockerfile*",
    "**/docker-compose*.yml",
    "**/docker-compose*.yaml",
    "**/CODEOWNERS",
    ".talismanrc",
    ".coderabbit.yaml",
)
REQUEST_MARKER = "<!-- stamp-gate:coderabbit-requested {sha} -->"
GATE_LOGIN = "github-actions[bot]"

PENDING_DEFAULT = "stamp-pending"

LABEL_COLORS = {
    "eligible": ("0e8a16", "Every rule in .github/stamp-policy.yml passed"),
    "needs_human": ("b60205", "A person reviews this pull request"),
    "pending": ("fbca04", "In the stamp lane; waiting on an AI reader, not on a person"),
    "request": ("1d76db", "The author asks the gate for its approval"),
    "agent_authored": ("5319e7", "An agent initiated this with no person in the loop; never stamped"),
    "do_not_stamp": ("000000", "Anyone's override: a person reviews this"),
}


def gh(*args: str, input_: str | None = None) -> str:
    result = subprocess.run(
        ["gh", *args], check=True, capture_output=True, text=True, input=input_
    )
    return result.stdout


def api(path: str, *extra: str) -> object:
    return json.loads(gh("api", "--paginate", "--slurp", path, *extra))


def api_list(path: str) -> list:
    pages = api(path)
    return [item for page in pages for item in page]


def post(path: str, payload: dict, method: str = "POST") -> str:
    return gh("api", "-X", method, path, "--input", "-", input_=json.dumps(payload))


def glob_to_regex(pattern: str) -> re.Pattern[str]:
    out = "^"
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if pattern.startswith("**/", i):
            out += "(?:.*/)?"
            i += 3
            continue
        if pattern.startswith("**", i):
            out += ".*"
            i += 2
            continue
        if c == "*":
            out += "[^/]*"
        elif c == "?":
            out += "[^/]"
        else:
            out += re.escape(c)
        i += 1
    return re.compile(out + "$")


def added_lines(files: list[dict]) -> list[str]:
    lines: list[str] = []
    for f in files:
        for line in (f.get("patch") or "").splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                lines.append(line[1:])
    return lines


def unresolved_threads_by(repo: str, number: int, login: str) -> int:
    owner, name = repo.split("/")
    query = """
    query($owner:String!,$name:String!,$number:Int!,$cursor:String){
      repository(owner:$owner,name:$name){
        pullRequest(number:$number){
          reviewThreads(first:100,after:$cursor){
            pageInfo{hasNextPage endCursor}
            nodes{isResolved isOutdated comments(first:1){nodes{author{login}}}}
          }}}}"""
    count = 0
    cursor = None
    while True:
        args = [
            "api",
            "graphql",
            "-f",
            f"query={query}",
            "-F",
            f"owner={owner}",
            "-F",
            f"name={name}",
            "-F",
            f"number={number}",
        ]
        if cursor:
            args += ["-F", f"cursor={cursor}"]
        data = json.loads(gh(*args))["data"]["repository"]["pullRequest"][
            "reviewThreads"
        ]
        for node in data["nodes"]:
            first = node["comments"]["nodes"]
            author = first[0]["author"]["login"] if first and first[0]["author"] else ""
            if author == login.removesuffix("[bot]") and not node["isResolved"]:
                count += 1
        if not data["pageInfo"]["hasNextPage"]:
            return count
        cursor = data["pageInfo"]["endCursor"]


def reader_reasons(repo: str, pr: dict, reader: dict, reviews: list[dict]) -> list[str]:
    """Why one reader does not satisfy the policy on the PR's head; empty when it does."""
    login = reader["login"]
    name = reader.get("name", login)
    number = pr["number"]
    head = pr["head"]["sha"]
    reasons: list[str] = []
    on_head = [
        r
        for r in reviews
        if r["user"]["login"] == login
        and r["commit_id"] == head
        and r["state"] != "DISMISSED"
    ]
    if reader.get("require_review_on_head", True) and not on_head:
        comments = api_list(f"repos/{repo}/issues/{number}/comments")
        last = next(
            (c["body"] for c in reversed(comments) if c["user"]["login"] == login), ""
        )
        why = f"no {name} review on head"
        if "rate limited by coderabbit.ai" in last:
            why += " (last run: rate limited)"
        elif "skip review by coderabbit.ai" in last:
            why += " (last run: skipped)"
        reasons.append(why)
    refuse = reader.get("refuse_verdict")
    if refuse and any(refuse in (r.get("body") or "") for r in on_head):
        reasons.append(f"{name} says needs-human")
    if reader.get("require_threads_resolved", True):
        open_threads = unresolved_threads_by(repo, number, login)
        if open_threads:
            reasons.append(f"{open_threads} unresolved {name} thread(s)")
    return reasons


def reader_refusal(pr: dict, reader: dict, reviews: list[dict]) -> str | None:
    """A reader's refusal on the PR's head, which no other reader can outweigh."""
    refuse = reader.get("refuse_verdict")
    if not refuse:
        return None
    head = pr["head"]["sha"]
    for r in reviews:
        if (
            r["user"]["login"] == reader["login"]
            and r["commit_id"] == head
            and r["state"] != "DISMISSED"
            and refuse in (r.get("body") or "")
        ):
            return f"{reader.get('name', reader['login'])} says needs-human"
    return None


def readers_split(
    repo: str, pr: dict, readers: list[dict], reviews: list[dict]
) -> tuple[list[str], list[str]]:
    """The reader state as two kinds, because they earn different verdicts. A refusal is a
    reader's considered `needs-human` on this head and stands on its own; the rest are reasons
    the head is not read yet, which a reader clears without a person. Both empty means satisfied."""
    refusals = [
        why for reader in readers if (why := reader_refusal(pr, reader, reviews))
    ]
    if refusals:
        return refusals, []
    all_reasons: list[str] = []
    for reader in readers:
        reasons = reader_reasons(repo, pr, reader, reviews)
        if not reasons:
            return [], []
        all_reasons += reasons
    return [], all_reasons


def readers_state(
    repo: str, pr: dict, readers: list[dict], reviews: list[dict]
) -> list[str]:
    """Every reason no reader satisfies the policy, refusals first."""
    refusals, reasons = readers_split(repo, pr, readers, reviews)
    return refusals + reasons


def rule_reasons(
    pr: dict, files: list[dict], policy: dict, default_branch: str
) -> list[str]:
    """Every failing rule except the readers: base, author, labels, size, paths, title, diff."""
    reasons: list[str] = []
    if pr["base"]["ref"] != default_branch:
        reasons.append(f"base is {pr['base']['ref']}, not {default_branch}")

    author = pr["user"]["login"]
    if author in policy.get("refuse_authors", []):
        reasons.append(f"author {author} is never stamped")

    labels = {lab["name"] for lab in pr.get("labels", [])}
    for lab in policy.get("refuse_labels", []):
        if lab in labels:
            reasons.append(f"label {lab}")

    size = policy["size"]
    changed = sum(f["additions"] + f["deletions"] for f in files)
    if changed > size["max_changed_lines"]:
        reasons.append(f"{changed} changed lines > {size['max_changed_lines']}")
    if len(files) > size["max_files"]:
        reasons.append(f"{len(files)} files > {size['max_files']}")

    floor = [(p, glob_to_regex(p)) for p in FLOOR_PATHS]
    floor_hits: list[str] = []
    for f in files:
        for pattern, rx in floor:
            if rx.match(f["filename"]) and pattern not in floor_hits:
                floor_hits.append(pattern)
    for pattern in floor_hits:
        reasons.append(f"touches {pattern} (fleet floor)")

    risky = [
        (p, glob_to_regex(p))
        for p in policy.get("risky_paths", [])
        if p not in FLOOR_PATHS
    ]
    hit_patterns: list[str] = []
    for f in files:
        for pattern, rx in risky:
            if rx.match(f["filename"]) and pattern not in hit_patterns:
                hit_patterns.append(pattern)
    for pattern in hit_patterns:
        reasons.append(f"touches {pattern}")

    for pattern in policy.get("deny_title", []):
        if re.search(pattern, pr.get("title") or "", re.IGNORECASE):
            reasons.append(f"title matches /{pattern}/")

    diff = "\n".join(added_lines(files))
    for pattern in policy.get("deny_diff", []):
        if re.search(pattern, diff):
            reasons.append(f"diff adds /{pattern}/")
    return reasons


def evaluate(
    repo: str,
    pr: dict,
    files: list[dict],
    policy: dict,
    default_branch: str,
    reviews: list[dict] | None = None,
) -> list[str]:
    if reviews is None:
        reviews = api_list(f"repos/{repo}/pulls/{pr['number']}/reviews")
    return rule_reasons(pr, files, policy, default_branch) + readers_state(
        repo, pr, policy["readers"], reviews
    )


def request_state(pr: dict, policy: dict, events: list[dict]) -> tuple[bool, list[str]]:
    """Whether the author has asked for the stamp, and why the ask does not count if not."""
    request = policy["labels"]["request"]
    labels = {lab["name"] for lab in pr.get("labels", [])}
    if request not in labels:
        return False, []
    reasons: list[str] = []
    refused = [lab for lab in policy.get("refuse_labels", []) if lab in labels]
    if refused:
        reasons.append(
            f"{request} requested with {', '.join(refused)}; the fleet does not stamp itself"
        )
    if policy["approve"].get("request_label_by_author_only", True):
        labeled = [
            e
            for e in events
            if e.get("event") == "labeled"
            and (e.get("label") or {}).get("name") == request
        ]
        actor = (labeled[-1].get("actor") or {}).get("login") if labeled else None
        if actor and actor != pr["user"]["login"]:
            reasons.append(f"{request} added by {actor}, not the author")
    return True, reasons


def human_dismissed_on_head(own_on_head: list[dict], events: list[dict]) -> str | None:
    """Login of a person who dismissed the gate's review on this head, if anyone did."""
    ids = {r["id"] for r in own_on_head if r["state"] == "DISMISSED"}
    for e in reversed(events):
        if e.get("event") != "review_dismissed":
            continue
        review_id = (e.get("dismissed_review") or {}).get("review_id")
        actor = (e.get("actor") or {}).get("login")
        if review_id in ids and actor and actor != GATE_LOGIN:
            return actor
    return None


@dataclass
class Plan:
    label: str
    dismiss: list[dict] = field(default_factory=list)
    approve: bool = False
    request_coderabbit: bool = False
    line: str = ""


def decide(
    pr: dict,
    policy: dict,
    rules: list[str],
    refusals: list[str],
    readers: list[str],
    requested: bool,
    request_reasons: list[str],
    own: list[dict],
    events: list[dict],
) -> Plan:
    """The writes the gate makes for this state, computed before any of them happen."""
    head = pr["head"]["sha"]
    blocking = rules + refusals
    reasons = blocking + readers
    eligible = not reasons
    if not requested:
        label = ""
    elif blocking:
        label = policy["labels"]["needs_human"]
    elif readers:
        label = pending_label(policy)
    else:
        label = policy["labels"]["eligible"]
    plan = Plan(label=label)
    approved_on_head = [
        r for r in own if r["state"] == "APPROVED" and r["commit_id"] == head
    ]
    own_on_head = [r for r in own if r["commit_id"] == head]
    plan.dismiss = [
        r for r in own if r["state"] == "APPROVED" and r["commit_id"] != head
    ]

    short = head[:7]
    verdict = f"`{label}`" if label else "no verdict"
    if eligible:
        line = f"**stamp:** {verdict} at `{short}` — every rule in `.github/stamp-policy.yml` passed."
    else:
        line = f"**stamp:** {verdict} at `{short}` — " + "; ".join(reasons) + "."

    enabled = bool(policy["approve"].get("enabled"))
    request_label = policy["labels"]["request"]
    if not requested:
        plan.dismiss += approved_on_head
        line += f" Add the `{request_label}` label to ask the gate for its approval."
    elif request_reasons:
        plan.dismiss += approved_on_head
        line += " " + "; ".join(request_reasons) + "; a person reviews."
    elif not eligible:
        plan.dismiss += approved_on_head
        wants = any(r.get("request_on_stamp") for r in policy["readers"])
        if not rules and wants:
            plan.request_coderabbit = True
            line += " CodeRabbit review requested for this head."
        line += " Approval waits."
    else:
        dismisser = human_dismissed_on_head(own_on_head, events)
        if dismisser:
            line += f" The gate's approval was dismissed by {dismisser}; a person reviews from here."
        elif not enabled:
            plan.dismiss += approved_on_head
            line += (
                " Would approve; approval is off in the policy, so a person approves."
            )
        elif approved_on_head:
            line += " Approved by the gate."
        else:
            plan.approve = True
            line += " Approved by the gate."
    plan.line = line
    return plan


def ensure_labels(repo: str, policy: dict) -> None:
    names = {
        "eligible": policy["labels"]["eligible"],
        "needs_human": policy["labels"]["needs_human"],
        "pending": pending_label(policy),
        "request": policy["labels"]["request"],
    }
    for key, name in list(names.items()) + [
        (lab.replace("-", "_"), lab) for lab in policy.get("refuse_labels", [])
    ]:
        color, description = LABEL_COLORS.get(key, ("ededed", ""))
        try:
            post(
                f"repos/{repo}/labels",
                {"name": name, "color": color, "description": description},
            )
        except subprocess.CalledProcessError as err:
            if "422" not in err.stderr:
                raise


def remove_label(repo: str, number: int, name: str) -> None:
    try:
        gh("api", "-X", "DELETE", f"repos/{repo}/issues/{number}/labels/{name}")
    except subprocess.CalledProcessError as err:
        if "404" not in err.stderr:
            raise


def set_labels(repo: str, number: int, add: str, remove: list[str]) -> None:
    """`add` is empty on a pull request whose author has not asked for a stamp: the gate holds
    no verdict on it and writes no label, while still clearing any verdict it wrote before."""
    if add:
        gh(
            "api",
            "-X",
            "POST",
            f"repos/{repo}/issues/{number}/labels",
            "-f",
            f"labels[]={add}",
        )
    for name in remove:
        remove_label(repo, number, name)


def pending_label(policy: dict) -> str:
    """`normalize_policy` defaults this, but `gate_one` reads a policy it never normalized."""
    return policy["labels"].get("pending", PENDING_DEFAULT)


def verdict_labels(policy: dict) -> list[str]:
    """The three labels the gate itself writes; the request label belongs to the author."""
    return [
        policy["labels"]["eligible"],
        policy["labels"]["needs_human"],
        pending_label(policy),
    ]


def upsert_comment(repo: str, number: int, body: str) -> None:
    comments = api_list(f"repos/{repo}/issues/{number}/comments")
    mine = next(
        (
            c
            for c in comments
            if c["user"]["login"] == GATE_LOGIN and MARKER in (c.get("body") or "")
        ),
        None,
    )
    payload = {"body": f"{MARKER}\n{body}"}
    if mine:
        post(f"repos/{repo}/issues/comments/{mine['id']}", payload, method="PATCH")
    else:
        post(f"repos/{repo}/issues/{number}/comments", payload)


def request_coderabbit(repo: str, number: int, head: str) -> bool:
    """Post `@coderabbitai review` once per head; True when the comment was posted now."""
    marker = REQUEST_MARKER.format(sha=head)
    comments = api_list(f"repos/{repo}/issues/{number}/comments")
    if any(marker in (c.get("body") or "") for c in comments):
        return False
    post(
        f"repos/{repo}/issues/{number}/comments",
        {"body": f"{marker}\n@coderabbitai review"},
    )
    return True


def dismiss(repo: str, number: int, review: dict, head: str) -> None:
    message = f"stamp: dismissed by the gate; approved at {review['commit_id'][:7]}, head is {head[:7]}"
    if review["commit_id"] == head:
        message = (
            "stamp: dismissed by the gate; the policy no longer passes on this head"
        )
    post(
        f"repos/{repo}/pulls/{number}/reviews/{review['id']}/dismissals",
        {"message": message, "event": "DISMISS"},
        method="PUT",
    )


def approve(repo: str, number: int, head: str, policy_sha: str, reader: str) -> None:
    body = (
        f"stamp: approved at {head[:7]} under policy {policy_sha[:7]}; reader: {reader}. "
        "Dismissed automatically on the next push, label change or failed rule."
    )
    post(
        f"repos/{repo}/pulls/{number}/reviews",
        {"event": "APPROVE", "commit_id": head, "body": body},
    )


def satisfied_reader(
    repo: str, pr: dict, readers: list[dict], reviews: list[dict]
) -> str:
    for reader in readers:
        if not reader_reasons(repo, pr, reader, reviews):
            return reader.get("name", reader["login"])
    return "none"


def normalize_policy(policy: dict) -> dict:
    """Bring a label-only policy up to the shape the gate reads, or say what is missing."""
    labels = policy.get("labels")
    if (
        not isinstance(labels, dict)
        or not labels.get("eligible")
        or not labels.get("needs_human")
    ):
        raise SystemExit(
            "stamp policy: `labels.eligible` and `labels.needs_human` are required"
        )
    labels.setdefault("request", "stamp")
    labels.setdefault("pending", PENDING_DEFAULT)
    policy.setdefault(
        "approve", {"enabled": False, "request_label_by_author_only": True}
    )
    if "readers" not in policy and isinstance(policy.get("coderabbit"), dict):
        legacy = policy["coderabbit"]
        policy["readers"] = [
            {
                "name": "CodeRabbit",
                "login": legacy.get("login", "coderabbitai[bot]"),
                "require_review_on_head": legacy.get("require_review_on_head", True),
                "require_threads_resolved": legacy.get(
                    "require_threads_resolved", True
                ),
            }
        ]
    if not isinstance(policy.get("readers"), list) or not policy["readers"]:
        raise SystemExit(
            "stamp policy: no `readers:` block (and no legacy `coderabbit:` block to read as one); "
            "list the reader logins the gate accepts"
        )
    if "size" not in policy:
        raise SystemExit(
            "stamp policy: `size` with `max_changed_lines` and `max_files` is required"
        )
    return policy


def main() -> int:
    repo = os.environ["REPO"]
    default_branch = os.environ["DEFAULT_BRANCH"]
    policy_path = os.environ["POLICY"]
    with open(policy_path) as fh:
        policy = normalize_policy(yaml.safe_load(fh))
    policy_sha = (
        os.environ.get("POLICY_SHA")
        or subprocess.run(
            ["git", "rev-parse", f"HEAD:{policy_path}"],
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
    )
    raw_number = os.environ.get("PR_NUMBER", "").strip()
    if raw_number:
        return gate_one(repo, int(raw_number), default_branch, policy, policy_sha)
    numbers = [
        p["number"] for p in api_list(f"repos/{repo}/pulls?state=open&per_page=100")
    ]
    failed: list[int] = []
    for number in numbers:
        try:
            gate_one(repo, number, default_branch, policy, policy_sha)
        except Exception as err:  # noqa: BLE001
            print(f"#{number}: gate failed: {err}")
            failed.append(number)
    if failed:
        print("gate failed on: " + ", ".join(f"#{n}" for n in failed))
        return 1
    return 0


def gate_one(
    repo: str, number: int, default_branch: str, policy: dict, policy_sha: str
) -> int:

    pr = json.loads(gh("api", f"repos/{repo}/pulls/{number}"))
    dry_run = os.environ.get("DRY_RUN") == "1"
    head = pr["head"]["sha"]
    if pr["draft"]:
        print(
            f"#{number} is a draft; no verdict, labels cleared, any gate approval dismissed"
        )
        if not dry_run:
            for name in verdict_labels(policy):
                remove_label(repo, number, name)
            reviews = api_list(f"repos/{repo}/pulls/{number}/reviews")
            for r in reviews:
                if r["user"]["login"] == GATE_LOGIN and r["state"] == "APPROVED":
                    dismiss(repo, number, r, head)
        return 0
    if pr["state"] != "open" and not dry_run:
        print(f"#{number} is {pr['state']}; no verdict")
        return 0

    files = api_list(f"repos/{repo}/pulls/{number}/files")
    reviews = api_list(f"repos/{repo}/pulls/{number}/reviews")
    events = api_list(f"repos/{repo}/issues/{number}/events")
    own = [r for r in reviews if r["user"]["login"] == GATE_LOGIN]

    rules = rule_reasons(pr, files, policy, default_branch)
    refusals, readers = readers_split(repo, pr, policy["readers"], reviews)
    requested, request_reasons = request_state(pr, policy, events)
    plan = decide(
        pr, policy, rules, refusals, readers, requested, request_reasons, own, events
    )
    stale = [name for name in verdict_labels(policy) if name != plan.label]

    if dry_run:
        for r in plan.dismiss:
            print(f"would dismiss review {r['id']} at {r['commit_id'][:7]}")
        if plan.request_coderabbit:
            print("would request a CodeRabbit review")
        if plan.approve:
            print(f"would approve at {head[:7]}")
    else:
        ensure_labels(repo, policy)
        for r in plan.dismiss:
            dismiss(repo, number, r, head)
        set_labels(repo, number, plan.label, stale)
        if plan.request_coderabbit:
            request_coderabbit(repo, number, head)
        if plan.approve:
            approve(
                repo,
                number,
                head,
                policy_sha,
                satisfied_reader(repo, pr, policy["readers"], reviews),
            )
        if policy.get("comment", {}).get("enabled", True):
            upsert_comment(repo, number, plan.line)

    print(plan.line)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as fh:
            fh.write(plan.line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

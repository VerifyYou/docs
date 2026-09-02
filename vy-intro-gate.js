/* Controls whether the home cinematic intro plays, and builds the cascading bot swarm.
   Mintlify auto-includes any root .js file (runs after the page is interactive). The intro is
   display:none by default (see style.css); this opts IN by adding .vy-intro-play to <html>.

   ALWAYS_PLAY = true -> plays on every load (dev/review). Flip to false before the prod push
   for once-per-browser. ?intro (or ?replay) on the URL force-replays and clears the flag. */
(function () {
  var ALWAYS_PLAY = false; // once per browser in prod; ?intro or the Replay button force it.
  try {
    var p = (location.pathname || '').replace(/\/+$/, '').toLowerCase();
    if (p !== '/learn/why-humancheck') return; // play on the Why HumanCheck page
    var KEY = 'vy_intro_seen_v3';
    var forceReplay = /(?:[?&#])(?:intro|replay)/i.test(location.search + location.hash);
    if (forceReplay) { try { localStorage.removeItem(KEY); } catch (e) {} }
    if (ALWAYS_PLAY || forceReplay || !localStorage.getItem(KEY)) {
      document.documentElement.classList.add('vy-intro-play');
      if (!ALWAYS_PLAY && !forceReplay) localStorage.setItem(KEY, '1');
      // Drop the play class once the curtain has lifted, so the hidden docs chrome (and the
      // reveal) only apply during the intro - not on every later article you navigate to.
      setTimeout(function () { document.documentElement.classList.remove('vy-intro-play'); }, 24500);
      // buildSwarm();  // disabled: React strips JS-injected bots; cascade must live in markup
    }
  } catch (e) { /* fail closed */ }

  /* Cascade: start with a couple of bots at the computer, then each bot spawns 4-6 MORE from
     its own spot, two generations deep, in a rapid random sequence - a runaway multiplication
     that drives home "one becomes many". Built in JS so the markup stays small. */
  function buildSwarm() {
    var fig = document.querySelector('.vy-intro-figure');
    if (!fig) return;
    var BOT = '<svg viewBox="0 0 140 165" fill="none"><path class="vy-bot-ant" d="M70 26L70 12"/>'
      + '<path class="vy-bot-dot" d="M66.5 9a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0 -7 0"/>'
      + '<path d="M55 26h30a9 9 0 0 1 9 9v22a9 9 0 0 1 -9 9h-30a9 9 0 0 1 -9 -9v-22a9 9 0 0 1 9 -9z"/>'
      + '<path class="vy-bot-eye" d="M55.5 46a4.5 4.5 0 1 0 9 0a4.5 4.5 0 1 0 -9 0"/>'
      + '<path class="vy-bot-eye" d="M75.5 46a4.5 4.5 0 1 0 9 0a4.5 4.5 0 1 0 -9 0"/>'
      + '<path d="M58 58L82 58" stroke-width="4"/>'
      + '<path d="M58 74h24a6 6 0 0 1 6 6v28a6 6 0 0 1 -6 6h-24a6 6 0 0 1 -6 -6v-28a6 6 0 0 1 6 -6z"/>'
      + '<path d="M52 84L38 100"/><path d="M88 84L102 100"/><path d="M62 114L62 146"/><path d="M78 114L78 146"/></svg>';
    var R = Math.random;
    var all = [];
    var gen = [ {x:0,y:0,px:0,py:0,t:5.85}, {x:0,y:0,px:0,py:0,t:6.0}, {x:0,y:0,px:0,py:0,t:6.15} ];
    gen.forEach(function (b) { all.push(b); });
    for (var g = 0; g < 2; g++) {
      var next = [];
      gen.forEach(function (parent) {
        var n = 4 + Math.floor(R() * 3); // 4-6 children each
        for (var i = 0; i < n; i++) {
          var ang = R() * Math.PI * 2;
          var dist = (g === 0 ? 70 : 55) + R() * 65;
          var c = {
            px: parent.x, py: parent.y,
            x: Math.max(-220, Math.min(220, parent.x + Math.cos(ang) * dist)),
            y: Math.max(-152, Math.min(152, parent.y + Math.sin(ang) * dist)),
            t: parent.t + 0.16 + R() * 0.22
          };
          next.push(c); all.push(c);
        }
      });
      gen = next;
      if (all.length > 60) break; // safety cap
    }
    var html = all.map(function (b) {
      var s = (0.34 + R() * 0.2).toFixed(2);
      return '<div class="vy-mbot" style="--x:' + b.x.toFixed(0) + 'px;--y:' + b.y.toFixed(0)
        + 'px;--px:' + b.px.toFixed(0) + 'px;--py:' + b.py.toFixed(0) + 'px;--s:' + s
        + ';animation-delay:' + b.t.toFixed(2) + 's,' + (b.t + 0.7).toFixed(2) + 's">' + BOT + '</div>';
    }).join('');
    // Append a NEW swarm React doesn't own (so it can't revert it), and hide the static one.
    var js = document.createElement('div');
    js.className = 'vy-swarm vy-swarm-js';
    js.innerHTML = html;
    fig.appendChild(js);
    document.documentElement.classList.add('vy-cascade');
  }
})();

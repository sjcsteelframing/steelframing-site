/* global.js — Steel Framing */

// ── Scroll reveal ─────────────────────────────────────────────────────────────
(function () {
  if (!('IntersectionObserver' in window)) return;

  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('section').forEach(function (sec) {
    if (sec.getBoundingClientRect().top > window.innerHeight) {
      sec.classList.add('reveal');
      obs.observe(sec);
    }
  });

  // Safety fallback
  setTimeout(function () {
    document.querySelectorAll('.reveal:not(.visible)').forEach(function (el) {
      el.classList.add('visible');
    });
  }, 2500);
})();

// ── Gallery auto-scroll + dots ────────────────────────────────────────────────
(function () {
  document.querySelectorAll('.horizontal-gallery').forEach(function (gallery) {
    var track = gallery.querySelector('.gallery-track');
    if (!track) return;

    // Build dots
    var cards = track.querySelectorAll('.gallery-card');
    var dots = null;
    if (cards.length > 1) {
      var dotsEl = document.createElement('div');
      dotsEl.className = 'gallery-dots';
      cards.forEach(function (_, i) {
        var dot = document.createElement('button');
        dot.className = 'gallery-dot' + (i === 0 ? ' active' : '');
        dot.setAttribute('aria-label', 'Foto ' + (i + 1));
        dot.setAttribute('type', 'button');
        dot.addEventListener('click', function () {
          var cw = cards[0].offsetWidth + 16;
          track.scrollTo({ left: i * cw, behavior: 'smooth' });
        });
        dotsEl.appendChild(dot);
      });
      gallery.appendChild(dotsEl);
      dots = dotsEl;
    }

    function updateDots() {
      if (!dots || !cards.length) return;
      var cw = cards[0].offsetWidth + 16;
      var idx = Math.min(Math.round(track.scrollLeft / cw), cards.length - 1);
      dots.querySelectorAll('.gallery-dot').forEach(function (d, i) {
        d.classList.toggle('active', i === idx);
      });
    }

    track.addEventListener('scroll', updateDots, { passive: true });

    // Auto-scroll
    var DELAY = 3200;
    var timer;

    function scroll() {
      var maxScroll = track.scrollWidth - track.clientWidth;
      if (maxScroll <= 0) return;
      if (track.scrollLeft >= maxScroll - 4) {
        track.scrollTo({ left: 0, behavior: 'smooth' });
      } else {
        var step = cards.length ? cards[0].offsetWidth + 16 : 200;
        track.scrollBy({ left: step, behavior: 'smooth' });
      }
    }

    function start() { timer = setInterval(scroll, DELAY); }
    function stop()  { clearInterval(timer); }

    start();
    gallery.addEventListener('mouseenter', stop);
    gallery.addEventListener('mouseleave', start);
    gallery.addEventListener('touchstart', stop, { passive: true });
    gallery.addEventListener('touchend', function () { setTimeout(start, 1500); }, { passive: true });
  });
})();

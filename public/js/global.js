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

// ── Lightbox para infográficos (.visual img) ──────────────────────────────────
(function () {
  // CSS injetado via JS — cobre todas as páginas sem alterar CSS individuais
  var style = document.createElement('style');
  style.textContent = [
    '.lbx-overlay{position:fixed;inset:0;background:rgba(0,0,0,.88);z-index:9999;display:flex;align-items:center;justify-content:center;cursor:zoom-out;opacity:0;transition:opacity .25s;pointer-events:none}',
    '.lbx-overlay.open{opacity:1;pointer-events:auto}',
    '.lbx-overlay img{max-width:92vw;max-height:92vh;border-radius:6px;box-shadow:0 20px 60px rgba(0,0,0,.5);cursor:default;object-fit:contain}',
    '.lbx-close{position:absolute;top:16px;right:20px;color:#fff;font-size:36px;line-height:1;cursor:pointer;background:none;border:none;padding:4px 10px;opacity:.75}',
    '.lbx-close:hover{opacity:1}',
    '.lbx-hint{position:absolute;bottom:18px;left:50%;transform:translateX(-50%);color:rgba(255,255,255,.55);font-size:13px;pointer-events:none;white-space:nowrap}',
    '.visual img{cursor:zoom-in}img.visual{cursor:zoom-in}.figure-wide img{cursor:zoom-in}.figure-button{cursor:zoom-in}.figure-button img{cursor:zoom-in}'
  ].join('');
  document.head.appendChild(style);

  // Overlay
  var overlay = document.createElement('div');
  overlay.className = 'lbx-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');

  var lbxImg = document.createElement('img');
  var closeBtn = document.createElement('button');
  closeBtn.className = 'lbx-close';
  closeBtn.innerHTML = '&times;';
  closeBtn.setAttribute('aria-label', 'Fechar imagem');

  var hint = document.createElement('div');
  hint.className = 'lbx-hint';
  hint.textContent = 'Clique fora ou pressione Esc para fechar';

  overlay.appendChild(lbxImg);
  overlay.appendChild(closeBtn);
  overlay.appendChild(hint);
  document.body.appendChild(overlay);

  function openLbx(src, alt) {
    lbxImg.src = src;
    lbxImg.alt = alt || '';
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    closeBtn.focus();
  }

  function closeLbx() {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  // Fechar ao clicar fora da imagem
  overlay.addEventListener('click', function (e) {
    if (e.target !== lbxImg) closeLbx();
  });
  closeBtn.addEventListener('click', closeLbx);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeLbx();
  });

  // Delegação: .visual img e img.visual (FISF + Steel vs Alvenaria)
  document.addEventListener('click', function (e) {
    var img = e.target.closest ? e.target.closest('.visual img') : null;
    if (!img && e.target.tagName === 'IMG' && e.target.closest && e.target.closest('.visual')) img = e.target;
    // img.visual: a propria img tem a classe visual (paginas Steel vs Alvenaria)
    if (!img && e.target.tagName === 'IMG' && e.target.classList && e.target.classList.contains('visual')) img = e.target;
    if (img) { e.preventDefault(); openLbx(img.src, img.alt); }
  });

  // Delegação: .figure-button[data-full] (páginas antigas)
  document.addEventListener('click', function (e) {
    var btn = e.target.closest ? e.target.closest('.figure-button') : null;
    if (btn && btn.getAttribute('data-full')) {
      e.preventDefault();
      openLbx(btn.getAttribute('data-full'), btn.getAttribute('aria-label') || '');
    }
  });

  // Delegação: .figure-wide img (mercado de investimento / airbnb)
  document.addEventListener('click', function (e) {
    var img = e.target.closest ? e.target.closest('.figure-wide img') : null;
    if (!img && e.target.tagName === 'IMG' && e.target.closest && e.target.closest('.figure-wide')) img = e.target;
    if (img) { e.preventDefault(); openLbx(img.src, img.alt); }
  });
})();

(function () {
  var WA = 'https://wa.me/5512991856900?text=';

  // Menu do celular
  var menuBtn = document.querySelector('.menu-btn');
  var nav = document.getElementById('site-nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = menuBtn.getAttribute('aria-expanded') !== 'true';
      menuBtn.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('open', open);
    });
  }

  // Menus Produtos e Serviços
  var ddBtns = Array.prototype.slice.call(document.querySelectorAll('.dd-btn'));
  function closeAll(except) {
    ddBtns.forEach(function (b) {
      if (b === except) return;
      b.setAttribute('aria-expanded', 'false');
      var p = document.getElementById(b.getAttribute('aria-controls'));
      if (p) p.hidden = true;
    });
  }
  ddBtns.forEach(function (b) {
    b.addEventListener('click', function (e) {
      e.stopPropagation();
      var p = document.getElementById(b.getAttribute('aria-controls'));
      var open = b.getAttribute('aria-expanded') !== 'true';
      closeAll(b);
      b.setAttribute('aria-expanded', String(open));
      if (p) p.hidden = !open;
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.dd')) closeAll(null);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var openBtn = ddBtns.filter(function (b) { return b.getAttribute('aria-expanded') === 'true'; })[0];
    closeAll(null);
    if (openBtn) openBtn.focus();
    if (nav && nav.classList.contains('open')) {
      nav.classList.remove('open');
      menuBtn.setAttribute('aria-expanded', 'false');
      menuBtn.focus();
    }
  });

  // Formulário de contato: monta a mensagem e abre o WhatsApp
  var form = document.getElementById('form-contato');
  if (form) {
    var interesse = new URLSearchParams(window.location.search).get('interesse');
    var sel = form.querySelector('[name="interesse"]');
    if (interesse && sel) {
      Array.prototype.forEach.call(sel.options, function (o) { if (o.value === interesse) sel.value = interesse; });
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var msg = 'Olá! Gostaria de conversar com a NOTA.\n\n' +
        'Nome: ' + d.get('nome') + '\n' +
        'Cidade / UF: ' + d.get('cidade') + '\n' +
        'Interesse: ' + d.get('interesse') + '\n' +
        'Quando pretendo começar: ' + d.get('prazo') + '\n' +
        'Tenho terreno: ' + d.get('terreno') + '\n' +
        'Faixa de investimento: ' + d.get('investimento') + '\n\n' +
        'Sobre a ideia:\n' + d.get('mensagem');
      var url = WA + encodeURIComponent(msg);
      var link = document.getElementById('wa-link');
      if (link) link.href = url;
      var result = document.getElementById('form-result');
      if (result) result.hidden = false;
      window.open(url, '_blank', 'noopener');
    });
  }
})();

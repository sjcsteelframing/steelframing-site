
(function () {
  const menuButton = document.querySelector('.menu-toggle');
  const menu = document.querySelector('.main-nav');

  if (menuButton && menu) {
    menuButton.addEventListener('click', () => {
      const open = menuButton.getAttribute('aria-expanded') === 'true';
      menuButton.setAttribute('aria-expanded', String(!open));
      menu.classList.toggle('is-open', !open);
    });
  }

  /*
   * MAPEAMENTO DE ASSETS DA HOME
   * ------------------------------------------------------------
   * Os nomes abaixo são temporários e centralizados de propósito.
   * Na consolidação final, basta trocar aqui pelos nomes EXATOS
   * existentes em /public/images/home.
   */
  const imageBase = window.location.protocol === 'file:'
    ? './public/images/home/'
    : '/images/home/';

  const HOME_IMAGES = {
    hero: imageBase + 'SF_hero_principal.png',
    'o-que-e-lsf': '/images/oque-e-lightsteelframing/lsf-significado-do-nome.png',
    comparacao: '/images/steelframing-vs-alvenaria/steel-framing-vs-alvenaria-criterios-de-decisao.png',
    airbnb: '/images/mercado-de-investimento/airbnb/i23.png',
    investimento: imageBase + 'SF_home_mercado-investimento.jpg'
  };

  document.querySelectorAll('[data-home-image]').forEach((element) => {
    const key = element.dataset.homeImage;
    const src = HOME_IMAGES[key];
    if (!src) return;

    const image = new Image();
    image.onload = () => {
      element.style.backgroundImage = `url("${src}")`;
      element.classList.add('has-image');
    };
    image.onerror = () => {
      element.classList.add('asset-pendente');
    };
    image.src = src;
  });
})();

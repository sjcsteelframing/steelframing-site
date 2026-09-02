
(() => {
  const btn = document.getElementById('menuBtn');
  const mobile = document.getElementById('mobileMenu');
  btn?.addEventListener('click', () => {
    const open = mobile.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
})();

// Lightbox das artes técnicas
(() => {
  const dialog = document.getElementById('technicalImageLightbox');
  if (!dialog) return;

  const modalImg = dialog.querySelector('[data-lightbox-image]');
  const title = dialog.querySelector('[data-lightbox-title]');
  const original = dialog.querySelector('[data-lightbox-original]');
  const closeBtn = dialog.querySelector('[data-lightbox-close]');

  document.querySelectorAll('.figure-button[data-full]').forEach(btn => {
    btn.addEventListener('click', () => {
      const img = btn.querySelector('img');
      modalImg.src = btn.dataset.full;
      modalImg.alt = img?.alt || '';
      title.textContent = img?.alt || 'Imagem técnica ampliada';
      original.href = btn.dataset.full;
      dialog.showModal();
    });
  });

  closeBtn?.addEventListener('click', () => dialog.close());

  dialog.addEventListener('click', event => {
    if (event.target === dialog) dialog.close();
  });

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && dialog.open) dialog.close();
  });
})();

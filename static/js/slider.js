(() => {
  const slider = document.getElementById('slider');
  if (!slider) return;

  const slides = Array.from(slider.querySelectorAll('.slide'));
  const prev = document.querySelector('.nav.prev');
  const next = document.querySelector('.nav.next');
  const dotsWrap = document.getElementById('slider-dots');

  let idx = slides.findIndex(s => s.classList.contains('is-active'));
  if (idx < 0) { idx = 0; slides[0]?.classList.add('is-active'); }

  // Crear dots
  slides.forEach((_, i) => {
    const b = document.createElement('button');
    b.setAttribute('aria-label', `Ir al slide ${i + 1}`);
    if (i === idx) b.classList.add('is-active');
    b.addEventListener('click', () => go(i, true));
    dotsWrap.appendChild(b);
  });

  function go(i, user = false) {
    slides[idx]?.classList.remove('is-active');
    dotsWrap.children[idx]?.classList?.remove('is-active');
    idx = (i + slides.length) % slides.length;
    slides[idx]?.classList.add('is-active');
    dotsWrap.children[idx]?.classList?.add('is-active');
    if (user) resetTimer();
  }

  prev.addEventListener('click', () => go(idx - 1, true));
  next.addEventListener('click', () => go(idx + 1, true));

  // Auto-rotación
  let timer = null;
  const interval = 5000;
  function startTimer(){ timer = setInterval(() => go(idx + 1), interval); }
  function resetTimer(){ if (timer) clearInterval(timer); startTimer(); }
  startTimer();
})();

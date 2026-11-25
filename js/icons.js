// ============================================================
// POSTPARTUM CARE — CUSTOM MOOD FACES (INLINE SVG)
// ============================================================

function moodFace(key, extraClass = '') {
  const faces = {
    senang: `
      <path d="M15.5 21c1.6-2.2 3.9-2.2 5.5 0"/>
      <path d="M27 21c1.6-2.2 3.9-2.2 5.5 0"/>
      <path d="M16 28.5c2.2 3.6 8 3.6 10.2 0"/>`,
    netral: `
      <circle cx="18" cy="21" r="1.7" fill="currentColor" stroke="none"/>
      <circle cx="30" cy="21" r="1.7" fill="currentColor" stroke="none"/>
      <path d="M17.5 31h13"/>`,
    lelah: `
      <path d="M14.5 21.5h6.5"/>
      <path d="M27 21.5h6.5"/>
      <path d="M19 31.5h10"/>
      <path d="M15.5 25.5l4.5 1"/>
      <path d="M32.5 25.5l-4.5 1"/>`,
    cemas: `
      <circle cx="18" cy="22" r="1.8" fill="currentColor" stroke="none"/>
      <circle cx="30" cy="22" r="1.8" fill="currentColor" stroke="none"/>
      <path d="M14 18l6 1.6"/>
      <path d="M34 18l-6 1.6"/>
      <path d="M19 31.5c1.7-1.6 3.3-1.6 5 0s3.3 1.6 5 0"/>`,
    sedih: `
      <circle cx="18" cy="22" r="1.8" fill="currentColor" stroke="none"/>
      <circle cx="30" cy="22" r="1.8" fill="currentColor" stroke="none"/>
      <path d="M14 19l6-2"/>
      <path d="M34 19l-6-2"/>
      <path d="M17 32.5c2.4-3.6 8.6-3.6 11 0"/>`
  };

  const inner = faces[key] || faces.netral;
  const classes = ['mood-face', extraClass].filter(Boolean).join(' ');

  return `<svg class="${classes}" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="24" cy="24" r="20"/>${inner}</svg>`;
}

function hydrateMoodFaces(root = document) {
  root.querySelectorAll('[data-mood-face]').forEach(el => {
    el.innerHTML = moodFace(el.getAttribute('data-mood-face'));
  });
}

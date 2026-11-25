// ============================================================
// POSTPARTUM CARE — GUIDED INFORMATION (EDUKASI)
// ============================================================

let activeCategory = 'all';

function renderArticles() {
  const container = document.getElementById('articles-container');
  if (!container) return;

  const searchVal = (document.getElementById('article-search-input')?.value || '').toLowerCase();

  const filtered = state.articles.filter(a => {
    const matchCat = (activeCategory === 'all') || (a.category === activeCategory);
    const matchSearch = a.title.toLowerCase().includes(searchVal) ||
      a.snippet.toLowerCase().includes(searchVal);
    return matchCat && matchSearch;
  });

  if (filtered.length === 0) {
    container.innerHTML = `<div class="empty-state grid-empty">Tidak ditemukan artikel untuk kata kunci tersebut.</div>`;
    return;
  }

  container.innerHTML = filtered.map(a => `
    <div class="article-card" onclick="openArticleModal(${a.id})">
      <div class="article-thumb" style="background: linear-gradient(135deg, #FBD9E5, #F283AF);">
        <span class="article-category">${a.catLabel}</span>
      </div>
      <div class="article-body">
        <div class="article-meta"><i class="fa-regular fa-clock" aria-hidden="true"></i> ${a.readTime} • ${a.author}</div>
        <h3 class="article-title">${a.title}</h3>
        <p class="article-snippet">${a.snippet}</p>
        <span class="read-more">Baca Panduan Lengkap <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></span>
      </div>
    </div>
  `).join('');
}

function filterArticles() {
  renderArticles();
}

function filterCategory(btn, cat) {
  activeCategory = cat;
  document.querySelectorAll('.cat-pill').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  renderArticles();
}

renderArticles();

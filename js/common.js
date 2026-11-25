// ============================================================
// POSTPARTUM CARE — SHARED APP SHELL & AUTH
// ============================================================

const AUTH_STORAGE_KEY = 'postpartumAuthUser';
const PROFILES_STORAGE_KEY = 'postpartumProfiles';
const MOOD_STORAGE_KEY = 'postpartumMoodHistory';

let currentUser = null;
let confirmCallback = null;

// --- Auth Storage ---
function getStoredProfile(email) {
  if (!email) return null;

  try {
    const profiles = JSON.parse(localStorage.getItem(PROFILES_STORAGE_KEY) || '{}');
    return profiles[email.toLowerCase()] || null;
  } catch {
    return null;
  }
}

function saveStoredProfile(email, profile) {
  if (!email) return;

  try {
    const profiles = JSON.parse(localStorage.getItem(PROFILES_STORAGE_KEY) || '{}');
    profiles[email.toLowerCase()] = profile;
    localStorage.setItem(PROFILES_STORAGE_KEY, JSON.stringify(profiles));
  } catch (err) {
    console.error('Gagal menyimpan profil:', err);
  }
}

function getAuthUser() {
  if (currentUser) return currentUser;

  try {
    const stored = JSON.parse(localStorage.getItem(AUTH_STORAGE_KEY));
    if (stored) {
      const profile = getStoredProfile(stored.email);
      currentUser = profile
        ? { ...stored, ...profile, email: stored.email, role: stored.role, roleLabel: stored.roleLabel }
        : stored;
    }
  } catch { }

  return currentUser;
}

function setAuthUser(user) {
  currentUser = user;
  try {
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user));
  } catch { }
  syncAuthUI();
}

function clearAuthUser() {
  currentUser = null;
  try {
    localStorage.removeItem(AUTH_STORAGE_KEY);
  } catch { }
  syncAuthUI();
}

// --- Mood History Storage ---
function getStoredMoodHistory() {
  try {
    const raw = localStorage.getItem(MOOD_STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : null;
  } catch {
    return null;
  }
}

function saveMoodHistory(items) {
  try {
    localStorage.setItem(MOOD_STORAGE_KEY, JSON.stringify(items));
  } catch (err) {
    console.error('Gagal menyimpan riwayat mood:', err);
  }
}

function todayStamp() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

// --- Shared UI Sync ---
function updateAvatarElement(element, user) {
  if (!element) return;

  element.innerHTML = '';
  element.classList.toggle('has-photo', Boolean(user && user.avatar));

  if (user && user.avatar) {
    const img = document.createElement('img');
    img.src = user.avatar;
    img.alt = `Foto profil ${user.name || ''}`.trim();
    element.appendChild(img);
  } else {
    element.innerText = user && user.name ? user.name.charAt(0).toUpperCase() : '?';
  }
}

function syncAuthUI() {
  const user = getAuthUser();
  const nameEl = document.getElementById('header-user-name');
  const avatarEl = document.getElementById('header-user-avatar');
  const authBtn = document.getElementById('header-auth-btn');
  const chip = document.getElementById('header-user-chip');
  const phaseEl = document.getElementById('header-user-phase');
  const isIbu = !user || user.role === 'ibu';
  const phaseDay = user && user.phaseDay !== '' && user.phaseDay !== undefined && user.phaseDay !== null
    ? Number(user.phaseDay)
    : null;
  const heroGreeting = document.getElementById('hero-greeting');
  const heroPhase = document.getElementById('hero-phase');
  const moodName = document.getElementById('mood-user-name');
  const journalLock = document.getElementById('journal-lock-user');
  const displayName = user ? user.name : 'Ibu Rani';

  if (nameEl) nameEl.innerText = user ? user.name : 'Tamu';
  updateAvatarElement(avatarEl, user);

  if (authBtn) {
    authBtn.innerHTML = user
      ? '<i class="fa-solid fa-right-from-bracket" aria-hidden="true"></i> Keluar'
      : '<i class="fa-solid fa-right-to-bracket" aria-hidden="true"></i> Masuk';
  }

  if (chip) {
    chip.title = user ? `Masuk sebagai ${user.name} • Klik untuk edit profil` : 'Belum masuk';
    chip.classList.toggle('active', currentPage() === 'profile.html');
  }

  if (moodName) moodName.innerText = displayName;
  if (journalLock) journalLock.innerText = displayName;

  if (heroGreeting) heroGreeting.innerText = `Halo, ${displayName}!`;
  if (heroPhase) {
    heroPhase.hidden = !isIbu;
    if (isIbu) {
      heroPhase.innerText = phaseDay !== null
        ? `Hari ke-${phaseDay} Masa Pascapersalinan (Fase Adaptasi Awal)`
        : 'Hari ke-12 Masa Pascapersalinan (Fase Adaptasi Awal)';
    }
  }

  if (phaseEl) {
    if (user && isIbu && phaseDay !== null) {
      phaseEl.innerText = `Hari ke-${phaseDay} Pemulihan`;
      phaseEl.hidden = false;
    } else {
      phaseEl.hidden = true;
    }
  }
}

function handleAuthAction() {
  const user = getAuthUser();

  if (!user) {
    window.location.href = 'login.html';
    return;
  }

  showConfirm({
    title: 'Keluar dari Akun?',
    message: 'Yakin ingin keluar? Data mood dan jurnal tetap tersimpan di perangkat ini.',
    confirmLabel: 'Ya, Keluar',
    danger: true,
    icon: 'fa-right-from-bracket',
    onConfirm: () => {
      clearAuthUser();
      window.location.href = 'login.html';
    }
  });
}

// --- Toast ---
function showToast(msg) {
  const toast = document.getElementById('toast');
  if (!toast) return;

  toast.innerText = msg;
  toast.classList.add('show');
  setTimeout(() => {
    toast.classList.remove('show');
  }, 3500);
}

// --- Header & Navigation ---
function currentPage() {
  const path = window.location.pathname.split('/').pop();
  return path && path.length ? path : 'index.html';
}

function navItems() {
  return [
    { page: 'index.html', label: 'Beranda', icon: 'fa-house' },
    { page: 'mood.html', label: 'Mood Check-In', icon: 'fa-face-smile' },
    { page: 'journal.html', label: 'Daily Journal', icon: 'fa-book-open' },
    { page: 'relaxation.html', label: 'Micro-Relaxation', icon: 'fa-headphones' },
    { page: 'edukasi.html', label: 'Edukasi', icon: 'fa-book-medical' },
    { page: 'bantuan.html', label: 'Bantuan Profesional', icon: 'fa-user-doctor' }
  ];
}

function brandMarkup(target = 'index.html') {
  return `
    <a class="brand-logo" href="${target}">
      <span class="logo-icon"><i class="fa-solid fa-spa" aria-hidden="true"></i></span>
      <div class="logo-text">
        <span class="logo-title">PostpartumCare</span>
        <span class="logo-sub">Pendamping Ibu Pascapersalinan</span>
      </div>
    </a>`;
}

function renderHeader() {
  const mount = document.getElementById('app-header');
  if (!mount) return;

  const page = currentPage();
  const isAuthPage = page === 'login.html' || page === 'register.html';

  if (isAuthPage) {
    mount.innerHTML = `
      <header class="app-header">
        <div class="header-container">${brandMarkup('login.html')}</div>
      </header>`;
    return;
  }

  const links = navItems().map(item => `
    <a class="nav-item${item.page === page ? ' active' : ''}" href="${item.page}">
      <i class="nav-icon fa-solid ${item.icon}" aria-hidden="true"></i> ${item.label}
    </a>`).join('');

  mount.innerHTML = `
    <header class="app-header">
      <div class="header-container">
        ${brandMarkup('index.html')}
        <nav class="nav-links">${links}</nav>
        <div class="header-actions">
          <a class="user-chip" id="header-user-chip" href="profile.html">
            <div class="user-avatar" id="header-user-avatar">?</div>
            <div class="user-meta">
              <span class="user-name" id="header-user-name">Ibu</span>
            </div>
          </a>
          <button class="btn btn-sm btn-outline header-auth-btn" id="header-auth-btn" onclick="handleAuthAction()"></button>
        </div>
      </div>
    </header>`;
}

function mountSharedUI() {
  if (!document.getElementById('toast')) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.id = 'toast';
    toast.innerText = 'Pesan notifikasi';
    document.body.appendChild(toast);
  }

  if (!document.getElementById('article-modal')) {
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
      <div class="modal-backdrop" id="article-modal" onclick="closeArticleModal(event)">
        <div class="modal-content">
          <button class="modal-close" onclick="closeArticleModalDirect()" aria-label="Tutup">
            <i class="fa-solid fa-xmark" aria-hidden="true"></i>
          </button>
          <div class="modal-category" id="modal-cat">Kategori</div>
          <h2 class="modal-title" id="modal-title">Judul</h2>
          <div class="modal-author" id="modal-author"></div>
          <div class="modal-body" id="modal-body"></div>
          <div class="modal-footer">
            <button class="btn btn-primary" id="modal-footer-btn" onclick="closeArticleModalDirect()">Selesai Membaca</button>
          </div>
        </div>
      </div>`;
    document.body.appendChild(wrapper.firstElementChild);
  }

  if (!document.getElementById('confirm-modal')) {
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
      <div class="modal-backdrop" id="confirm-modal" onclick="handleConfirmBackdrop(event)">
        <div class="modal-content confirm-modal" role="dialog" aria-modal="true" aria-labelledby="confirm-title">
          <div class="confirm-icon" id="confirm-icon">
            <i class="fa-solid fa-triangle-exclamation" aria-hidden="true"></i>
          </div>
          <h2 class="confirm-title" id="confirm-title">Konfirmasi</h2>
          <p class="confirm-message" id="confirm-message">Apakah Anda yakin?</p>
          <div class="confirm-actions">
            <button type="button" class="btn btn-outline" id="confirm-cancel-btn" onclick="closeConfirm()">Batalkan</button>
            <button type="button" class="btn btn-danger" id="confirm-ok-btn" onclick="acceptConfirm()">Ya</button>
          </div>
        </div>
      </div>`;
    document.body.appendChild(wrapper.firstElementChild);
  }
}

// --- Confirmation Dialog ---
function showConfirm(options = {}) {
  const {
    title = 'Konfirmasi',
    message = 'Apakah Anda yakin?',
    confirmLabel = 'Ya',
    cancelLabel = 'Batalkan',
    danger = false,
    icon = 'fa-triangle-exclamation',
    onConfirm = null
  } = options;

  const modal = document.getElementById('confirm-modal');
  if (!modal) return;

  confirmCallback = typeof onConfirm === 'function' ? onConfirm : null;

  document.getElementById('confirm-title').innerText = title;
  document.getElementById('confirm-message').innerText = message;

  const iconEl = document.getElementById('confirm-icon');
  iconEl.className = 'confirm-icon' + (danger ? ' danger' : '');
  iconEl.innerHTML = `<i class="fa-solid ${icon}" aria-hidden="true"></i>`;

  const okBtn = document.getElementById('confirm-ok-btn');
  okBtn.className = danger ? 'btn btn-danger' : 'btn btn-primary';
  okBtn.innerText = confirmLabel;

  const cancelBtn = document.getElementById('confirm-cancel-btn');
  cancelBtn.innerText = cancelLabel;

  modal.classList.add('open');
}

function closeConfirm() {
  const modal = document.getElementById('confirm-modal');
  if (modal) modal.classList.remove('open');
  confirmCallback = null;
}

function acceptConfirm() {
  const callback = confirmCallback;
  closeConfirm();
  if (callback) callback();
}

function handleConfirmBackdrop(event) {
  if (event.target.id === 'confirm-modal') closeConfirm();
}

// --- Shared Article Modal ---
function openArticleModal(id) {
  const article = state.articles.find(a => a.id === id);
  if (!article) return;

  if (typeof closeJournalAudio === 'function') closeJournalAudio();

  document.getElementById('modal-cat').innerText = article.catLabel;
  document.getElementById('modal-title').innerText = article.title;
  document.getElementById('modal-author').innerText = `Oleh: ${article.author} • Ditinjau secara medis`;
  document.getElementById('modal-body').innerHTML = article.content;

  const footerBtn = document.getElementById('modal-footer-btn');
  if (footerBtn) footerBtn.innerText = 'Selesai Membaca';

  document.getElementById('article-modal').classList.add('open');
}

function closeArticleModal(e) {
  if (e.target.id === 'article-modal') {
    closeArticleModalDirect();
  }
}

function closeArticleModalDirect() {
  if (typeof closeJournalAudio === 'function') closeJournalAudio();
  const modal = document.getElementById('article-modal');
  if (modal) modal.classList.remove('open');
}

// --- Init ---
function initCommon() {
  renderHeader();
  mountSharedUI();
  syncAuthUI();

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;

    if (document.getElementById('confirm-modal')?.classList.contains('open')) {
      closeConfirm();
      return;
    }

    closeArticleModalDirect();
  });
}

initCommon();

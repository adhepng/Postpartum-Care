// ============================================================
// POSTPARTUM CARE — BERANDA / DASHBOARD
// ============================================================

function renderDashboardMoodFaces() {
  const container = document.getElementById('dash-mood-faces');
  if (!container) return;

  container.innerHTML = MOOD_ORDER
    .map(key => `<span class="mood-face-wrap">${moodFace(key, 'mood-face--mini')}</span>`)
    .join('');
}

function updateDashboardMoodStatus() {
  const status = document.getElementById('dash-mood-status');
  if (!status) return;

  const today = todayStamp();
  const filledToday = state.moodHistory.some(item => item.dayStamp === today);

  if (filledToday) {
    status.className = 'card-status-badge ok-badge';
    status.innerHTML = '<i class="fa-solid fa-check" aria-hidden="true"></i> Sudah Diisi Hari Ini';
  } else {
    status.className = 'card-status-badge alert-badge';
    status.innerText = 'Belum Diisi Hari Ini';
  }
}

function initBeranda() {
  const stored = getStoredMoodHistory();
  if (stored && stored.length) {
    state.moodHistory = stored;
  } else {
    saveMoodHistory(state.moodHistory);
  }

  renderDashboardMoodFaces();
  updateDashboardMoodStatus();
}

initBeranda();

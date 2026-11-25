// ============================================================
// POSTPARTUM CARE — MOOD CHECK-IN
// ============================================================

const MOOD_MONTHS_SHORT = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
const MOOD_MONTHS_LONG = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
const MOOD_MONTH_INDEX = MOOD_MONTHS_SHORT.reduce((map, name, index) => {
  map[name.toLowerCase()] = index + 1;
  return map;
}, {});

let moodChartDate = todayStamp();

function selectMood(el) {
  document.querySelectorAll('.mood-option').forEach(opt => {
    opt.classList.remove('selected');
    const badge = opt.querySelector('.sel-mark');
    if (badge) badge.remove();
  });

  el.classList.add('selected');
  const mark = document.createElement('span');
  mark.className = 'sel-mark';
  mark.innerHTML = '<i class="fa-solid fa-check" aria-hidden="true"></i> Dipilih';
  el.appendChild(mark);

  const key = el.getAttribute('data-mood-key') || 'netral';
  state.selectedMoodKey = key;
  state.selectedMood = MOOD_OPTIONS[key]?.label || key;
}

function toggleChip(el) {
  el.classList.toggle('active');
}

function moodDateLabel() {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
  const now = new Date();
  return `Hari ini, ${now.getDate()} ${months[now.getMonth()]}`;
}

function saveMoodCheckin() {
  const note = document.getElementById('mood-note').value;
  const activeChips = Array.from(document.querySelectorAll('#factor-tags .tag-chip.active'))
    .map(c => c.innerText.replace(/[^\w\s]/gi, '').trim());
  const now = new Date();
  const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')} WIB`;

  const newItem = {
    date: moodDateLabel(),
    time: timeStr,
    moodKey: state.selectedMoodKey,
    tags: activeChips.join(', ') || 'Refleksi Diri',
    note: note || 'Tidak ada catatan tambahan.',
    color: '#C43670',
    dayStamp: todayStamp()
  };

  state.moodHistory.unshift(newItem);
  saveMoodHistory(state.moodHistory);

  moodChartDate = todayStamp();
  const chartDateInput = document.getElementById('mood-chart-date');
  if (chartDateInput) chartDateInput.value = moodChartDate;

  renderMoodHistory();

  if (typeof updateDashboardMoodStatus === 'function') {
    updateDashboardMoodStatus();
  }

  showToast('Catatan suasana hati berhasil disimpan!');
  document.getElementById('mood-note').value = '';
}

function renderMoodHistory() {
  const listEl = document.getElementById('mood-history-list');
  if (!listEl) return;

  listEl.innerHTML = state.moodHistory.slice(0, 5).map(item => {
    const mood = MOOD_OPTIONS[item.moodKey] || MOOD_OPTIONS.netral;

    return `
    <div class="history-card">
      <div class="hist-dot" style="background-color: ${item.color}"></div>
      <div class="hist-content">
        <div class="hist-top">
          <span class="hist-date">${item.date}</span>
          <span class="hist-time">${item.time}</span>
        </div>
        <div class="hist-mood">
          ${moodFace(item.moodKey, 'mood-face--sm')}
          <span>${mood.label}</span>
        </div>
        <div class="hist-tags">${item.tags}</div>
        <div class="hist-note">"${item.note}"</div>
      </div>
    </div>`;
  }).join('');

  renderMoodChart();
}

function escapeHtml(text) {
  return String(text ?? '').replace(/[&<>"']/g, ch => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[ch]));
}

function ensureMoodDayStamps(items) {
  const year = new Date().getFullYear();
  let changed = false;

  for (const item of items) {
    if (item.dayStamp) continue;
    const match = (item.date || '').match(/(\d{1,2})\s+([A-Za-z]{3})/);
    if (!match) continue;

    const month = MOOD_MONTH_INDEX[match[2].toLowerCase()];
    if (!month) continue;

    item.dayStamp = `${year}-${String(month).padStart(2, '0')}-${String(Number(match[1])).padStart(2, '0')}`;
    changed = true;
  }

  return changed;
}

function changeMoodChartDate(value) {
  moodChartDate = /^\d{4}-\d{2}-\d{2}$/.test(value) ? value : todayStamp();
  renderMoodChart();
}

function renderMoodChart() {
  const chart = document.getElementById('mood-chart');
  const summary = document.getElementById('mood-chart-summary');
  const legend = document.getElementById('mood-chart-legend');
  const detail = document.getElementById('mood-chart-detail');
  const dateInput = document.getElementById('mood-chart-date');
  if (!chart) return;

  if (dateInput && dateInput.value !== moodChartDate) dateInput.value = moodChartDate;

  const [year, month, selectedDay] = moodChartDate.split('-').map(Number);
  const daysInMonth = new Date(year, month, 0).getDate();
  const monthName = MOOD_MONTHS_LONG[month - 1] || '';
  const monthShort = MOOD_MONTHS_SHORT[month - 1] || '';

  const entriesByDay = new Map();
  for (const item of state.moodHistory) {
    if (!item.dayStamp) continue;
    const [itemYear, itemMonth, itemDay] = item.dayStamp.split('-').map(Number);
    if (itemYear !== year || itemMonth !== month) continue;
    if (!entriesByDay.has(itemDay)) entriesByDay.set(itemDay, item);
  }

  if (legend) {
    legend.innerHTML = MOOD_ORDER.map(key => `
      <span class="mood-legend-item">
        ${moodFace(key, 'mood-face--xs')}
        <span>${MOOD_OPTIONS[key].label}</span>
      </span>`).join('');
  }

  const columns = [];
  for (let day = 1; day <= daysInMonth; day++) {
    const item = entriesByDay.get(day);
    const isSelected = day === selectedDay;

    if (item) {
      const mood = MOOD_OPTIONS[item.moodKey] || MOOD_OPTIONS.netral;
      const score = MOOD_SCORES[item.moodKey] || 3;
      const height = Math.max(14, Math.round((score / 5) * 100));

      columns.push(`
        <div class="mood-chart-col${isSelected ? ' is-selected' : ''}" title="${day} ${monthShort} • ${mood.label}">
          <div class="mood-chart-track">
            <div class="mood-chart-bar mood-chart-bar--${item.moodKey}" style="height: ${height}%">
              ${moodFace(item.moodKey, 'mood-face--xs')}
            </div>
          </div>
          <span class="mood-chart-label">${day}</span>
        </div>`);
    } else {
      columns.push(`
        <div class="mood-chart-col is-empty${isSelected ? ' is-selected' : ''}" title="${day} ${monthShort} • Belum ada catatan">
          <div class="mood-chart-track">
            <div class="mood-chart-empty-bar"></div>
          </div>
          <span class="mood-chart-label">${day}</span>
        </div>`);
    }
  }
  chart.innerHTML = columns.join('');

  const monthEntries = [...entriesByDay.values()];

  if (summary) {
    if (monthEntries.length === 0) {
      summary.innerHTML = `Belum ada catatan di ${monthName} ${year}`;
    } else {
      const average = monthEntries.reduce((total, item) => total + (MOOD_SCORES[item.moodKey] || 3), 0) / monthEntries.length;
      const nearest = MOOD_ORDER
        .slice()
        .sort((a, b) => Math.abs(MOOD_SCORES[a] - average) - Math.abs(MOOD_SCORES[b] - average))[0];
      summary.innerHTML = `Rata-rata: <strong>${MOOD_OPTIONS[nearest].label}</strong> • ${monthEntries.length} hari tercatat`;
    }
  }

  if (detail) {
    const item = entriesByDay.get(selectedDay);

    if (!item) {
      detail.innerHTML = `<p class="mood-chart-detail-empty">Belum ada catatan mood pada ${selectedDay} ${monthName} ${year}.</p>`;
    } else {
      const mood = MOOD_OPTIONS[item.moodKey] || MOOD_OPTIONS.netral;
      detail.innerHTML = `
        <div class="mood-chart-detail-head">
          ${moodFace(item.moodKey, 'mood-face--sm')}
          <div>
            <strong>${selectedDay} ${monthName} ${year}</strong>
            <span>${mood.label}${item.time ? ' • ' + escapeHtml(item.time) : ''}</span>
          </div>
        </div>
        ${item.note ? `<p>"${escapeHtml(item.note)}"</p>` : ''}
        ${item.tags ? `<span class="mood-chart-detail-tags">${escapeHtml(item.tags)}</span>` : ''}`;
    }
  }
}

function initMood() {
  hydrateMoodFaces();

  const stored = getStoredMoodHistory();
  if (stored && stored.length) {
    state.moodHistory = stored;
  } else {
    saveMoodHistory(state.moodHistory);
  }

  if (ensureMoodDayStamps(state.moodHistory)) {
    saveMoodHistory(state.moodHistory);
  }

  moodChartDate = todayStamp();
  const dateInput = document.getElementById('mood-chart-date');
  if (dateInput) {
    dateInput.value = moodChartDate;
    dateInput.max = todayStamp();
  }

  renderMoodHistory();
}

initMood();

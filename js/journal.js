// ============================================================
// POSTPARTUM CARE — DAILY JOURNAL, INDEXEDDB & VOICE NOTE
// ============================================================

const JOURNAL_DB_NAME = 'postpartumCareDB';
const JOURNAL_DB_VERSION = 1;
const JOURNAL_STORE = 'journals';
let journalDBPromise = null;

function openJournalDB() {
  if (journalDBPromise) return journalDBPromise;

  journalDBPromise = new Promise((resolve, reject) => {
    if (!('indexedDB' in window)) {
      reject(new Error('IndexedDB tidak didukung browser ini.'));
      return;
    }

    const request = indexedDB.open(JOURNAL_DB_NAME, JOURNAL_DB_VERSION);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains(JOURNAL_STORE)) {
        db.createObjectStore(JOURNAL_STORE, { keyPath: 'id' });
      }
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });

  return journalDBPromise;
}

async function loadJournalsFromDB() {
  const db = await openJournalDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(JOURNAL_STORE, 'readonly');
    const request = tx.objectStore(JOURNAL_STORE).getAll();
    request.onsuccess = () => resolve(request.result || []);
    request.onerror = () => reject(request.error);
  });
}

async function saveJournalToDB(entry) {
  const db = await openJournalDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(JOURNAL_STORE, 'readwrite');
    tx.objectStore(JOURNAL_STORE).put(entry);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

async function deleteJournalFromDB(id) {
  const db = await openJournalDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(JOURNAL_STORE, 'readwrite');
    tx.objectStore(JOURNAL_STORE).delete(id);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

// --- Voice Note Recorder ---
let mediaRecorder = null;
let recordingStream = null;
let recordedChunks = [];
let recordedBlob = null;
let recordedDuration = 0;
let recordingTimer = null;
let recordingSeconds = 0;
let isRecording = false;
let previewObjectUrl = null;
let journalAudioUrl = null;

function formatDuration(totalSeconds) {
  const seconds = Math.max(0, Math.floor(totalSeconds || 0));
  const minutes = Math.floor(seconds / 60);
  const remainder = seconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(remainder).padStart(2, '0')}`;
}

function getSupportedAudioMimeType() {
  if (typeof MediaRecorder === 'undefined' || typeof MediaRecorder.isTypeSupported !== 'function') {
    return '';
  }

  const candidates = [
    'audio/webm;codecs=opus',
    'audio/webm',
    'audio/ogg;codecs=opus',
    'audio/mp4',
    'audio/mpeg'
  ];

  return candidates.find(type => MediaRecorder.isTypeSupported(type)) || '';
}

function stopStreamTracks() {
  if (recordingStream) {
    recordingStream.getTracks().forEach(track => track.stop());
    recordingStream = null;
  }
}

function updateRecordUI() {
  const button = document.getElementById('vn-record-btn');
  const indicator = document.getElementById('vn-recording');

  if (button) {
    button.innerHTML = isRecording
      ? '<i class="fa-solid fa-stop" aria-hidden="true"></i> Selesai Rekam'
      : '<i class="fa-solid fa-microphone" aria-hidden="true"></i> Mulai Rekam';
    button.classList.toggle('recording', isRecording);
  }
  if (indicator) indicator.hidden = !isRecording;
}

function revokePreviewUrl() {
  if (previewObjectUrl) {
    URL.revokeObjectURL(previewObjectUrl);
    previewObjectUrl = null;
  }

  const audio = document.getElementById('vn-preview');
  if (audio) {
    audio.pause();
    audio.removeAttribute('src');
    audio.load();
  }
}

function resetVoiceNoteState() {
  recordedBlob = null;
  recordedDuration = 0;
  recordedChunks = [];
  revokePreviewUrl();

  const wrap = document.getElementById('vn-preview-wrap');
  if (wrap) wrap.hidden = true;

  const timer = document.getElementById('vn-timer');
  if (timer) timer.innerText = '00:00';
}

function showVoiceNotePreview(blob) {
  const wrap = document.getElementById('vn-preview-wrap');
  const audio = document.getElementById('vn-preview');
  if (!wrap || !audio) return;

  revokePreviewUrl();
  previewObjectUrl = URL.createObjectURL(blob);
  audio.src = previewObjectUrl;
  wrap.hidden = false;
}

async function startRecording() {
  if (isRecording) return;

  if (!window.isSecureContext) {
    showToast('Perekaman suara memerlukan HTTPS atau localhost.');
    return;
  }

  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || typeof MediaRecorder === 'undefined') {
    showToast('Browser ini belum mendukung perekaman suara.');
    return;
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recordingStream = stream;
    resetVoiceNoteState();
    recordedChunks = [];

    const mimeType = getSupportedAudioMimeType();
    mediaRecorder = mimeType ? new MediaRecorder(stream, { mimeType }) : new MediaRecorder(stream);
    mediaRecorder.ondataavailable = (event) => {
      if (event.data && event.data.size > 0) recordedChunks.push(event.data);
    };
    mediaRecorder.onstop = finalizeRecording;
    mediaRecorder.onerror = (event) => {
      console.error('MediaRecorder error:', event.error);
      showToast('Terjadi masalah saat merekam voice note.');
      stopRecording();
    };

    mediaRecorder.start();
    isRecording = true;
    recordingSeconds = 0;
    updateRecordUI();

    recordingTimer = setInterval(() => {
      recordingSeconds += 1;
      const timer = document.getElementById('vn-timer');
      if (timer) timer.innerText = formatDuration(recordingSeconds);
    }, 1000);

    showToast('Mulai merekam voice note...');
  } catch (err) {
    stopStreamTracks();
    mediaRecorder = null;
    isRecording = false;
    updateRecordUI();

    if (err.name === 'NotAllowedError' || err.name === 'SecurityError') {
      showToast('Izin mikrofon ditolak. Aktifkan izin mikrofon untuk merekam.');
    } else if (err.name === 'NotFoundError') {
      showToast('Mikrofon tidak ditemukan di perangkat ini.');
    } else {
      showToast('Tidak dapat mengakses mikrofon: ' + (err.message || err.name));
    }
  }
}

function stopRecording() {
  if (recordingTimer) {
    clearInterval(recordingTimer);
    recordingTimer = null;
  }

  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    try {
      mediaRecorder.stop();
    } catch (err) {
      console.error('Gagal menghentikan rekaman:', err);
    }
  }

  stopStreamTracks();
  isRecording = false;
  updateRecordUI();
}

function finalizeRecording() {
  const mimeType = (mediaRecorder && mediaRecorder.mimeType) || 'audio/webm';
  const blob = recordedChunks.length ? new Blob(recordedChunks, { type: mimeType }) : null;

  recordedChunks = [];
  mediaRecorder = null;
  isRecording = false;
  stopStreamTracks();

  if (recordingTimer) {
    clearInterval(recordingTimer);
    recordingTimer = null;
  }
  updateRecordUI();

  if (!blob || blob.size === 0) {
    showToast('Rekaman kosong, silakan coba lagi.');
    return;
  }

  recordedBlob = blob;
  recordedDuration = recordingSeconds;
  showVoiceNotePreview(blob);
  showToast(`Voice note (${formatDuration(recordedDuration)}) siap disimpan.`);
}

function toggleRecording() {
  if (isRecording) {
    stopRecording();
  } else {
    startRecording();
  }
}

function clearVoiceNote() {
  showConfirm({
    title: 'Hapus Voice Note?',
    message: 'Rekaman voice note yang belum disimpan akan dihapus dan tidak bisa dikembalikan.',
    confirmLabel: 'Ya, Hapus',
    danger: true,
    icon: 'fa-microphone-slash',
    onConfirm: () => {
      if (isRecording) stopRecording();
      resetVoiceNoteState();
      showToast('Voice note dihapus.');
    }
  });
}

// --- Journal Entries ---
function formatJournalDate(date = new Date()) {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'];
  return `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`;
}

async function saveJournalEntry() {
  if (isRecording) {
    showToast('Hentikan rekaman dulu sebelum menyimpan jurnal.');
    return;
  }

  const title = document.getElementById('journal-title').value.trim();
  const body = document.getElementById('journal-body').value.trim();
  const activeTags = Array.from(document.querySelectorAll('#journal-tags .tag-chip.active'))
    .map(c => c.innerText.trim());

  if (!body && !recordedBlob) {
    showToast('Isi catatan atau rekam voice note terlebih dahulu.');
    return;
  }

  const dateLabel = formatJournalDate();
  const finalTitle = title || (recordedBlob ? `Catatan Suara ${dateLabel}` : `Catatan ${dateLabel}`);
  const snippet = body
    ? (body.length > 100 ? body.substring(0, 97) + '...' : body)
    : `Catatan suara ${formatDuration(recordedDuration)}`;

  const newEntry = {
    id: Date.now(),
    createdAt: Date.now(),
    date: `${dateLabel} (Hari ini)`,
    title: finalTitle,
    tags: activeTags,
    snippet: snippet,
    full: body,
    audio: recordedBlob,
    audioDuration: recordedDuration
  };

  state.journals.unshift(newEntry);
  renderJournalFeed();
  resetJournalForm();
  showToast('Jurnal pribadi berhasil disimpan secara aman!');

  try {
    await saveJournalToDB(newEntry);
  } catch (err) {
    console.error('Gagal menyimpan jurnal ke IndexedDB:', err);
    showToast('Jurnal tersimpan di sesi ini, tetapi gagal disimpan permanen.');
  }
}

function resetJournalForm() {
  document.getElementById('journal-title').value = '';
  document.getElementById('journal-body').value = '';
  resetVoiceNoteState();
}

function requestResetJournalForm() {
  const title = document.getElementById('journal-title')?.value.trim() || '';
  const body = document.getElementById('journal-body')?.value.trim() || '';
  const hasVoice = Boolean(recordedBlob) || isRecording;

  if (!title && !body && !hasVoice) {
    resetJournalForm();
    return;
  }

  showConfirm({
    title: 'Reset Form Jurnal?',
    message: 'Teks dan rekaman yang belum disimpan akan hilang.',
    confirmLabel: 'Ya, Reset',
    danger: true,
    icon: 'fa-rotate-left',
    onConfirm: () => {
      if (isRecording) stopRecording();
      resetJournalForm();
      showToast('Form jurnal direset.');
    }
  });
}

function deleteJournal(id) {
  const entry = state.journals.find(j => j.id === id);
  const entryTitle = entry?.title ? `"${entry.title}"` : 'Catatan ini';

  showConfirm({
    title: 'Hapus Catatan Jurnal?',
    message: `${entryTitle} akan dihapus permanen dan tidak bisa dikembalikan.`,
    confirmLabel: 'Ya, Hapus',
    danger: true,
    icon: 'fa-trash-can',
    onConfirm: async () => {
      state.journals = state.journals.filter(j => j.id !== id);
      renderJournalFeed();
      showToast('Catatan jurnal telah dihapus.');

      try {
        await deleteJournalFromDB(id);
      } catch (err) {
        console.error('Gagal menghapus jurnal dari IndexedDB:', err);
      }
    }
  });
}

function filterJournal(query) {
  const q = query.toLowerCase();
  const filtered = state.journals.filter(j =>
    (j.title || '').toLowerCase().includes(q) ||
    (j.snippet || '').toLowerCase().includes(q) ||
    (j.tags || []).some(t => t.toLowerCase().includes(q))
  );
  renderJournalFeed(filtered);
}

function renderJournalFeed(items = state.journals) {
  const feedEl = document.getElementById('journal-feed');
  const countEl = document.getElementById('journal-count');
  if (!feedEl) return;

  if (countEl) countEl.innerText = `${items.length} Catatan`;

  if (items.length === 0) {
    feedEl.innerHTML = `<div class="empty-state">Tidak ada catatan yang sesuai.</div>`;
    return;
  }

  feedEl.innerHTML = items.map(j => {
    const hasAudio = j.audio instanceof Blob && j.audio.size > 0;
    const audioBadge = hasAudio
      ? `<div class="vn-badge"><i class="fa-solid fa-microphone" aria-hidden="true"></i> Voice Note • ${formatDuration(j.audioDuration)}</div>`
      : '';
    const snippet = j.snippet || (hasAudio ? `Catatan suara ${formatDuration(j.audioDuration)}` : '');

    return `
    <div class="journal-card-item">
      <div class="j-top">
        <span class="j-date">${j.date}</span>
        <span class="j-tags">${(j.tags || []).join(' ')}</span>
      </div>
      <h3 class="j-title">${j.title}</h3>
      ${audioBadge}
      <p class="j-snippet">${snippet}</p>
      <div class="j-actions">
        <button class="j-act-btn" onclick="openJournalModal(${j.id})"><i class="fa-solid fa-book-open" aria-hidden="true"></i> Baca Penuh</button>
        <button class="j-act-btn delete" onclick="deleteJournal(${j.id})"><i class="fa-solid fa-trash-can" aria-hidden="true"></i> Hapus</button>
      </div>
    </div>`;
  }).join('');
}

function closeJournalAudio() {
  const audio = document.getElementById('modal-journal-audio');
  if (audio) audio.pause();

  if (journalAudioUrl) {
    URL.revokeObjectURL(journalAudioUrl);
    journalAudioUrl = null;
  }
}

function openJournalModal(id) {
  const entry = state.journals.find(j => j.id === id);
  if (!entry) return;

  closeJournalAudio();

  const hasAudio = entry.audio instanceof Blob && entry.audio.size > 0;
  document.getElementById('modal-cat').innerText = 'Jurnal Pribadi';
  document.getElementById('modal-title').innerText = entry.title;
  const authorName = getAuthUser()?.name || 'Ibu Rani';
  document.getElementById('modal-author').innerText = `Ditulis oleh ${authorName} • Tersimpan Privat`;

  const audioHtml = hasAudio
    ? `<div class="modal-audio-block">
         <div class="modal-audio-label"><i class="fa-solid fa-microphone" aria-hidden="true"></i> Voice Note • ${formatDuration(entry.audioDuration)}</div>
         <audio class="modal-audio" id="modal-journal-audio" controls></audio>
       </div>`
    : '';
  const bodyHtml = entry.full
    ? `<p class="modal-journal-text">${entry.full}</p>`
    : `<p class="modal-journal-text empty"><em>Catatan ini hanya berisi voice note.</em></p>`;

  document.getElementById('modal-body').innerHTML = audioHtml + bodyHtml;

  const footerBtn = document.getElementById('modal-footer-btn');
  if (footerBtn) footerBtn.innerText = 'Selesai';

  if (hasAudio) {
    journalAudioUrl = URL.createObjectURL(entry.audio);
    document.getElementById('modal-journal-audio').src = journalAudioUrl;
  }

  document.getElementById('article-modal').classList.add('open');
}

function journalSortValue(entry) {
  if (typeof entry.createdAt === 'number') return entry.createdAt;
  return -entry.id;
}

async function initJournalStorage() {
  renderJournalFeed();

  try {
    const stored = await loadJournalsFromDB();
    if (stored.length > 0) {
      state.journals = stored.sort((a, b) => journalSortValue(b) - journalSortValue(a));
    } else {
      const seedTime = Date.now();
      state.journals = state.journals.map((entry, index) => ({
        ...entry,
        createdAt: seedTime - index * 1000
      }));

      for (const entry of state.journals) {
        await saveJournalToDB(entry);
      }
    }
  } catch (err) {
    console.error('IndexedDB tidak tersedia, jurnal hanya tersimpan di sesi ini:', err);
  }

  renderJournalFeed();
}

initJournalStorage();

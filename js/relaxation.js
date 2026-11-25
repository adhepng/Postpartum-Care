// ============================================================
// POSTPARTUM CARE — MICRO-RELAXATION PLAYER
// ============================================================

let audioTimer = null;
let currentSeconds = 0;
const totalDuration = 180; // 3 menit
let isPlaying = false;

function togglePlayAudio() {
  if (isPlaying) {
    pauseAudio();
  } else {
    playAudio();
  }
}

function setPlayIcon(playing) {
  const icon = document.getElementById('play-icon');
  if (icon) {
    icon.innerHTML = playing
      ? '<i class="fa-solid fa-pause" aria-hidden="true"></i>'
      : '<i class="fa-solid fa-play" aria-hidden="true"></i>';
  }

  const btn = document.getElementById('btn-play-pause');
  if (btn) btn.title = playing ? 'Jeda' : 'Putar';
}

function playAudio() {
  isPlaying = true;
  setPlayIcon(true);

  clearInterval(audioTimer);
  audioTimer = setInterval(() => {
    if (currentSeconds < totalDuration) {
      currentSeconds++;
      updateAudioProgress();
      updateBreathingVisual();
    } else {
      stopAudio();
      showToast('Sesi relaksasi 3 menit selesai. Semoga hatimu lebih tenang.');
    }
  }, 1000);
}

function pauseAudio() {
  isPlaying = false;
  setPlayIcon(false);
  clearInterval(audioTimer);
}

function stopAudio() {
  pauseAudio();
  currentSeconds = 0;
  updateAudioProgress();
  resetBreathingVisual();
}

function rewindAudio(sec) {
  currentSeconds = Math.max(0, currentSeconds - sec);
  updateAudioProgress();
}

function seekAudio(e) {
  const bg = e.currentTarget;
  const rect = bg.getBoundingClientRect();
  const clickX = e.clientX - rect.left;
  const pct = clickX / rect.width;
  currentSeconds = Math.floor(pct * totalDuration);
  updateAudioProgress();
}

function updateAudioProgress() {
  const min = Math.floor(currentSeconds / 60);
  const sec = currentSeconds % 60;
  document.getElementById('player-current-time').innerText =
    `${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;

  const pct = (currentSeconds / totalDuration) * 100;
  document.getElementById('player-progress').style.width = `${pct}%`;
}

function updateBreathingVisual() {
  const cycle = currentSeconds % 12; // 4s Tarik, 4s Tahan, 4s Hembus
  const circle = document.getElementById('breath-circle');
  const actionText = document.getElementById('breath-text');
  const countText = document.getElementById('breath-count');

  if (cycle < 4) {
    circle.className = 'breathing-circle-outer inhale';
    actionText.innerText = 'Tarik Napas...';
    countText.innerText = `${4 - cycle} Detik`;
  } else if (cycle < 8) {
    circle.className = 'breathing-circle-outer inhale';
    actionText.innerText = 'Tahan Sejenak...';
    countText.innerText = `${8 - cycle} Detik`;
  } else {
    circle.className = 'breathing-circle-outer exhale';
    actionText.innerText = 'Hembuskan Perlahan...';
    countText.innerText = `${12 - cycle} Detik`;
  }
}

function resetBreathingVisual() {
  const circle = document.getElementById('breath-circle');
  if (circle) circle.className = 'breathing-circle-outer';
  document.getElementById('breath-text').innerText = 'Tarik Napas';
  document.getElementById('breath-count').innerText = '4 Detik';
}

function selectSession(title) {
  document.getElementById('relax-track-title').innerText = title;
  stopAudio();
  document.querySelectorAll('.session-card').forEach(c => {
    const isThis = c.querySelector('.session-title').innerText.includes(title.substring(0, 15));
    c.classList.toggle('active-session', isThis);
    c.querySelector('.session-action').innerHTML = isThis
      ? '<i class="fa-solid fa-circle-check" aria-hidden="true"></i> Sedang Dipilih'
      : '<i class="fa-solid fa-play" aria-hidden="true"></i> Putar Sesi Ini';
  });
  playAudio();
  showToast(`Memulai: ${title}`);
}

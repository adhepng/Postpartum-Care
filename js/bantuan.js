// ============================================================
// POSTPARTUM CARE — PROFESSIONAL DIRECTORY & BOOKING
// ============================================================

let selectedProName = 'Rina Kusuma, M.Psi., Psikolog';
let selectedProSpec = 'Psikolog Klinis Perinatal & Trauma Salin';

function selectPro(el, name, spec, fee) {
  document.querySelectorAll('.pro-item').forEach(item => {
    item.classList.remove('selected');
    const btn = item.querySelector('.btn');
    if (btn) {
      btn.className = 'btn btn-sm btn-outline';
      btn.innerText = 'Pilih';
    }
  });

  el.classList.add('selected');
  const btn = el.querySelector('.btn');
  if (btn) {
    btn.className = 'btn btn-sm btn-primary';
    btn.innerHTML = '<i class="fa-solid fa-check" aria-hidden="true"></i> Dipilih';
  }

  selectedProName = name;
  selectedProSpec = spec;
  document.getElementById('chosen-pro-name').innerText = name;
  document.getElementById('chosen-pro-spec').innerText = spec;
  showToast(`Memilih ${name}`);
}

function selectTime(btn) {
  document.querySelectorAll('.time-slots .time-chip').forEach(c => c.classList.remove('active'));
  btn.classList.add('active');
}

function submitBooking() {
  const dateVal = document.getElementById('booking-date').value;
  const activeTime = document.querySelector('.time-slots .time-chip.active')?.innerText || '14:00 WIB';
  const mediaVal = document.getElementById('booking-media').value;
  const notes = document.getElementById('booking-notes').value;

  if (!dateVal) {
    showToast('Harap tentukan tanggal konsultasi.');
    return;
  }

  const card = document.getElementById('booking-status-card');
  card.innerHTML = `
    <div class="status-top">
      <span class="status-badge waiting"><i class="fa-solid fa-hourglass-half" aria-hidden="true"></i> Menunggu Konfirmasi</span>
      <span class="status-date">${dateVal} • ${activeTime}</span>
    </div>
    <h4 class="status-pro">${selectedProName}</h4>
    <p class="status-desc">Media: ${mediaVal}. Permintaan terkirim! Tenaga profesional akan mengonfirmasi dalam waktu maksimal 2 jam.</p>
  `;

  showToast('Permintaan sesi konsultasi berhasil dikirim!');
  document.getElementById('booking-notes').value = '';
}

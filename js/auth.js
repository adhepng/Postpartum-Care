// ============================================================
// POSTPARTUM CARE — LOGIN & REGISTER
// ============================================================

let selectedLoginRole = 'ibu';
let selectedRegRole = 'ibu';

function selectLoginRole(role) {
  selectedLoginRole = role;
  document.querySelectorAll('#tab-login .role-tab').forEach(tab => {
    tab.classList.toggle('active', tab.dataset.role === role);
  });
}

function handleLoginSubmit(event) {
  event.preventDefault();

  const email = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value;

  if (!email || !password) {
    showToast('Harap isi email dan kata sandi terlebih dahulu.');
    return;
  }

  const role = document.querySelector('#tab-login .role-tab.active')?.dataset.role || selectedLoginRole;
  const knownUsers = {
    'ibu.rani@postpartum.id': { name: 'Ibu Rani', roleLabel: 'Ibu Pascasalin' },
    'rina.kusuma@postpartum.id': { name: 'Rina Kusuma, M.Psi.', roleLabel: 'Tenaga Medis' },
    'admin@postpartum.id': { name: 'Administrator Sistem', roleLabel: 'Admin' }
  };

  const known = knownUsers[email.toLowerCase()];
  const fallbackName = email.split('@')[0].replace(/[._-]+/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  const roleLabels = { ibu: 'Ibu Pascasalin', pro: 'Tenaga Medis', admin: 'Admin' };

  const baseUser = {
    email,
    name: known ? known.name : fallbackName,
    role,
    roleLabel: known ? known.roleLabel : (roleLabels[role] || roleLabels.ibu)
  };
  const savedProfile = getStoredProfile(email);
  const defaultPhase = role === 'ibu' ? { phaseDay: 12 } : {};

  setAuthUser({
    ...baseUser,
    ...defaultPhase,
    ...(savedProfile || {}),
    email,
    role,
    roleLabel: baseUser.roleLabel
  });

  window.location.href = 'index.html';
}

function selectRegRole(role) {
  selectedRegRole = role;
  document.querySelectorAll('#tab-register .role-tab').forEach(tab => {
    tab.classList.toggle('active', tab.id === `reg-role-${role}`);
  });

  const birthDateGroup = document.getElementById('group-tgl-persalinan');
  const specializationGroup = document.getElementById('group-spesialisasi');
  const birthDateInput = document.getElementById('reg-birth-date');

  if (birthDateGroup) birthDateGroup.style.display = role === 'ibu' ? '' : 'none';
  if (specializationGroup) specializationGroup.style.display = role === 'pro' ? '' : 'none';

  if (birthDateInput) {
    birthDateInput.required = role === 'ibu';
    birthDateInput.disabled = role !== 'ibu';
  }
}

function handleRegisterSubmit(event) {
  event.preventDefault();

  const name = document.getElementById('reg-name').value.trim();
  const email = document.getElementById('reg-email').value.trim();
  const password = document.getElementById('reg-password').value;
  const passwordConfirm = document.getElementById('reg-password-confirm').value;
  const agree = document.getElementById('reg-agree').checked;

  if (!name || !email) {
    showToast('Harap lengkapi nama lengkap dan alamat email.');
    return;
  }

  if (password.length < 8) {
    showToast('Kata sandi minimal 8 karakter.');
    return;
  }

  if (password !== passwordConfirm) {
    showToast('Konfirmasi kata sandi tidak cocok.');
    return;
  }

  if (!agree) {
    showToast('Anda harus menyetujui Syarat & Ketentuan untuk mendaftar.');
    return;
  }

  const isPro = selectedRegRole === 'pro';
  const specialization = document.getElementById('reg-specialization')?.value.trim();
  const deliveryDate = !isPro ? (document.getElementById('reg-birth-date')?.value || '') : '';
  const phaseDay = calculatePhaseDay(deliveryDate);

  const initialProfile = {
    name,
    avatar: '',
    phaseDay,
    bio: '',
    phone: '',
    birthDate: ''
  };

  setAuthUser({
    email,
    role: selectedRegRole,
    roleLabel: isPro ? 'Tenaga Medis' : 'Ibu Pascasalin',
    specialization: isPro ? specialization : '',
    ...initialProfile
  });
  saveStoredProfile(email, initialProfile);

  window.location.href = 'index.html';
}

function calculatePhaseDay(dateString) {
  if (!dateString) return '';

  const start = new Date(`${dateString}T00:00:00`);
  if (Number.isNaN(start.getTime())) return '';

  const diff = Math.floor((Date.now() - start.getTime()) / 86400000);
  return diff >= 0 ? diff : '';
}

// ============================================================
// POSTPARTUM CARE — PROFILE PAGE
// ============================================================

let profileDraftAvatar = '';

function initProfilePage() {
  const user = getAuthUser();
  if (!user) {
    window.location.href = 'login.html';
    return;
  }

  profileDraftAvatar = user.avatar || '';

  document.getElementById('profile-name-input').value = user.name || '';
  document.getElementById('profile-email-input').value = user.email || '';
  document.getElementById('profile-phase-input').value =
    user.phaseDay !== '' && user.phaseDay !== undefined && user.phaseDay !== null ? user.phaseDay : '';
  document.getElementById('profile-phone-input').value = user.phone || '';
  document.getElementById('profile-birth-input').value = user.birthDate || '';
  document.getElementById('profile-bio-input').value = user.bio || '';
  document.getElementById('profile-photo-input').value = '';

  const birthInput = document.getElementById('profile-birth-input');
  if (birthInput) birthInput.max = new Date().toISOString().slice(0, 10);

  updateProfileAvatarPreview();
  updateProfileBioCounter();
}

function updateProfileAvatarPreview() {
  const preview = document.getElementById('profile-edit-avatar');
  if (!preview) return;

  const name = document.getElementById('profile-name-input')?.value.trim() || '';

  preview.innerHTML = '';
  preview.classList.toggle('has-photo', Boolean(profileDraftAvatar));

  if (profileDraftAvatar) {
    const img = document.createElement('img');
    img.src = profileDraftAvatar;
    img.alt = 'Preview foto profil';
    preview.appendChild(img);
  } else {
    preview.innerText = name ? name.charAt(0).toUpperCase() : '?';
  }

  const removeBtn = document.getElementById('profile-photo-remove');
  if (removeBtn) removeBtn.hidden = !profileDraftAvatar;
}

function updateProfileBioCounter() {
  const bio = document.getElementById('profile-bio-input');
  const counter = document.getElementById('profile-bio-counter');
  if (bio && counter) counter.innerText = `${bio.value.length}/160`;
}

function handleProfilePhotoChange(event) {
  const file = event.target.files && event.target.files[0];
  if (!file) return;

  if (!file.type.startsWith('image/')) {
    showToast('Pilih file gambar (JPG/PNG).');
    event.target.value = '';
    return;
  }

  if (file.size > 5 * 1024 * 1024) {
    showToast('Ukuran foto maksimal 5 MB.');
    event.target.value = '';
    return;
  }

  const reader = new FileReader();
  reader.onload = () => {
    const img = new Image();
    img.onload = () => {
      const size = 256;
      const canvas = document.createElement('canvas');
      canvas.width = size;
      canvas.height = size;
      const ctx = canvas.getContext('2d');
      const scale = Math.max(size / img.width, size / img.height);
      const width = img.width * scale;
      const height = img.height * scale;

      ctx.drawImage(img, (size - width) / 2, (size - height) / 2, width, height);
      profileDraftAvatar = canvas.toDataURL('image/jpeg', 0.85);
      updateProfileAvatarPreview();
      showToast('Foto profil siap disimpan.');
    };
    img.onerror = () => showToast('Gagal membaca gambar. Coba file lain.');
    img.src = reader.result;
  };
  reader.onerror = () => showToast('Gagal membaca file foto.');
  reader.readAsDataURL(file);
}

function removeProfilePhoto() {
  if (!profileDraftAvatar) return;

  showConfirm({
    title: 'Hapus Foto Profil?',
    message: 'Foto profil akan dihapus saat perubahan disimpan.',
    confirmLabel: 'Ya, Hapus',
    danger: true,
    icon: 'fa-camera',
    onConfirm: () => {
      profileDraftAvatar = '';
      const photoInput = document.getElementById('profile-photo-input');
      if (photoInput) photoInput.value = '';

      updateProfileAvatarPreview();
      showToast('Foto profil akan dihapus saat disimpan.');
    }
  });
}

function saveProfileChanges(event) {
  event.preventDefault();

  const user = getAuthUser();
  if (!user) return;

  const name = document.getElementById('profile-name-input').value.trim();
  const phaseValue = document.getElementById('profile-phase-input').value.trim();
  const phone = document.getElementById('profile-phone-input').value.trim();
  const birthDate = document.getElementById('profile-birth-input').value;
  const bio = document.getElementById('profile-bio-input').value.trim();

  if (!name) {
    showToast('Nama lengkap tidak boleh kosong.');
    return;
  }

  if (phone && !/^[0-9+\-\s()]{8,20}$/.test(phone)) {
    showToast('Format nomor telepon tidak valid.');
    return;
  }

  let phaseDay = '';
  if (phaseValue !== '') {
    const parsed = Number(phaseValue);
    if (!Number.isFinite(parsed) || parsed < 0 || parsed > 365) {
      showToast('Hari pemulihan harus berada di antara 0-365.');
      return;
    }
    phaseDay = parsed;
  }

  const editableProfile = {
    name,
    avatar: profileDraftAvatar || '',
    phaseDay,
    bio,
    phone,
    birthDate
  };

  setAuthUser({ ...user, ...editableProfile });
  saveStoredProfile(user.email, editableProfile);
  syncAuthUI();
  showToast('Profil berhasil diperbarui.');
}

initProfilePage();

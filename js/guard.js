// ============================================================
// POSTPARTUM CARE — ROUTE GUARD (loaded early in <head>)
// ============================================================
(function () {
  var PUBLIC_PAGES = ['login.html', 'register.html'];
  var page = window.location.pathname.split('/').pop() || 'index.html';
  var isPublic = PUBLIC_PAGES.indexOf(page) !== -1;
  var user = null;

  try {
    user = JSON.parse(localStorage.getItem('postpartumAuthUser'));
  } catch (e) {
    user = null;
  }

  if (!user && !isPublic) {
    window.location.replace('login.html');
  } else if (user && isPublic) {
    window.location.replace('index.html');
  }
})();

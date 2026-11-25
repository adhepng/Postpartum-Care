# UI Checklist

## Pages to verify / update
- Landing page
- Login / Register page
- Beranda (home)
- Mood Check‑in
- Daily Journal
- Guided Information
- Konten Relaksasi
- Profesional Access
- Profile

## Required items
- **Edit Profile** button/link on Profile page (add if missing)
- Global font set to **Poppins** (e.g., in `src/styles/global.css` or theme provider)

### Action plan
1. Search UI component files (`**/*.tsx` / `**/*.js`) for each page.
2. Identify missing `Edit Profile` UI on the Profile page.
3. Add `font-family: 'Poppins', sans-serif;` to the global stylesheet or theme configuration.
4. Verify each page renders correctly after changes.

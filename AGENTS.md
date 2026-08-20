# AGENTS.md

## Cursor Cloud specific instructions

ARTNOART is a **static site** (plain HTML/CSS/JS) with **Python stdlib-only** tests. There
are no third-party dependencies to install and no build step — the browser loads
`index.html`, `index.css`, and `index.js` directly.

Services and commands (all standard, already documented in `README.md`):

- Dev server: `python3 -m http.server 4173` from the repo root, then open
  `http://127.0.0.1:4173`. It serves the site and the download assets under
  `assets/downloads/`.
- Tests: `python3 tests/test_downloads.py` (validates the catalog, HTTP download
  routes, and HTML wiring). Expect `9/9 OK`.

Non-obvious notes:

- There is **no linter configured** and **no build step**; "lint/build" is not
  applicable to this repo.
- The two download voies (`data-dwet-mode="direct"` and `="fetch"`) and the audio
  player are the core feature. The Fetch route uses `fetch` → `Blob` →
  `URL.createObjectURL`; the DWET browser module is exposed on `window.DWET`.
- Google Fonts require network on first load; the page still works offline with
  fallback fonts.
- WAV extracts are intentionally ~5 s technical jingles, not masters.

# AGENTS.md

## Cursor Cloud specific instructions

ARTNOART is a **static website** (plain HTML/CSS/JS) with a Python `unittest` test
suite. There is no package manager, no build step, and no third-party
dependencies — only the Python 3 standard library is used. The cloud VM ships
with a suitable Python 3 (3.12), so no install step is required.

Key files: `index.html`, `index.css`, `index.js` (the browser DWET download
module, exposed on `window.DWET`), `assets/downloads/catalog.json` (the machine
catalog of downloadable files), and `tests/test_downloads.py`.

### Run (dev server)
Serve the site from the repo root; the app is fully static so any static server
works. The documented command (see `README.md`) is:

```bash
python3 -m http.server 4173
```

Then open http://127.0.0.1:4173/index.html . There is no hot reload — after
editing files, just refresh the browser.

### Test
```bash
python3 tests/test_downloads.py
```

The suite starts its own ephemeral `http.server` on a random port, so it does
**not** need the dev server running (and won't conflict with it). It validates
`catalog.json` integrity, HTTP download routes (Direct + Fetch voies), byte
identity between disk and network, WAV headers/duration, and HTML wiring.

### Lint
No linter/formatter is configured in this repo (no ESLint, Prettier, Ruff, or
Flake8 config, and no `package.json`). There is no lint command to run.

### Non-obvious notes
- Google Fonts are loaded from the network on first page load; without egress
  the page still works but falls back to system fonts.
- Audio playback requires a real browser (it uses the `Audio` element); the
  Python tests only verify the WAV files, not playback.
- There is no backend: no download counters, no auth.

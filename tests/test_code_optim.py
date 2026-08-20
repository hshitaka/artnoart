#!/usr/bin/env python3
"""Verrouille les corrections d’optimisation du code (audit _hub)."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "index.css").read_text(encoding="utf-8")
JS = (ROOT / "index.js").read_text(encoding="utf-8")

FONT_HREF = (
    "https://fonts.googleapis.com/css2?"
    "family=IBM+Plex+Mono:wght@400&family=Manrope:wght@400;700"
    "&family=Syne:wght@800&display=swap"
)


class CodeOptimTests(unittest.TestCase):
    def test_google_fonts_only_request_used_weights(self) -> None:
        self.assertIn(FONT_HREF, HTML)
        self.assertNotIn("Manrope:wght@400;500;600;700", HTML)
        self.assertNotIn("Syne:wght@700;800", HTML)
        self.assertNotIn("IBM+Plex+Mono:wght@400;500", HTML)
        self.assertIn("display=swap", HTML)
        self.assertEqual(HTML.count("fonts.googleapis.com/css2"), 1)

    def test_fetch_does_not_bypass_http_cache(self) -> None:
        self.assertNotIn("no-store", JS)
        self.assertNotIn('cache: "reload"', JS)
        self.assertGreaterEqual(len(re.findall(r"\bfetch\s*\(", JS)), 2)

    def test_player_is_reused_and_inline(self) -> None:
        self.assertEqual(JS.count("new Audio("), 1)
        self.assertIn("player.playsInline = true", JS)
        self.assertNotIn("activeAudio", JS)

    def test_track_cards_contain_layout(self) -> None:
        self.assertRegex(CSS, r"\.track\s*\{[^}]*contain:\s*layout style")

    def test_player_still_does_not_blank_src(self) -> None:
        self.assertNotIn('player.src = ""', JS)
        self.assertNotIn("player.src = ''", JS)
        self.assertNotIn('audio.src = ""', JS)


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Les fiches village (kb + dd) existent et portent les quatre blocs."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "_kb"

FICHES = [
    KB / "dj" / "FONCTION.md",
    KB / "ableton" / "FONCTION.md",
    KB / "prod" / "FONCTION.md",
    KB / "mix" / "FONCTION.md",
    KB / "voix" / "FONCTION.md",
    KB / "perf" / "FONCTION.md",
    KB / "pedago" / "FONCTION.md",
    KB / "outils" / "FONCTION.md",
    KB / "village" / "README.md",
    KB / "village" / "bo-ia.md",
    KB / "village" / "dd-a2dd.md",
    KB / "village" / "dd-artnoart.md",
    KB / "village" / "dd-jukbike.md",
    KB / "village" / "dd-genre-formater.md",
    KB / "village" / "kb-cuisine.md",
    KB / "village" / "kb-herbo.md",
]


class VillageFichesTests(unittest.TestCase):
    def test_fiches_exist(self) -> None:
        for path in FICHES:
            self.assertTrue(path.is_file(), path)

    def test_metier_fiches_have_cest_and_pas_and_servi(self) -> None:
        for path in FICHES:
            if path.name == "README.md":
                continue
            text = path.read_text(encoding="utf-8")
            self.assertIn("# Fiche", text, path)
            self.assertIn("## C’est", text, path)
            self.assertIn("## C’est pas", text, path)
            self.assertIn("## Déjà servi", text, path)

    def test_village_index_lists_kb_and_dd(self) -> None:
        text = (KB / "village" / "README.md").read_text(encoding="utf-8")
        for name in (
            "kb-dj",
            "dd-a2dd",
            "dd-artnoart",
            "dd-jukbike",
            "dd-genre-formater",
            "bo-ia",
            "kb-cuisine",
            "kb-herbo",
        ):
            self.assertIn(name, text)

    def test_closed_cartes_have_no_invented_links(self) -> None:
        for name in ("kb-cuisine.md", "kb-herbo.md"):
            text = (KB / "village" / name).read_text(encoding="utf-8")
            self.assertIn("fermée", text)
            self.assertIn("Aucun geste nommé", text)

    def test_root_readme_points_to_village(self) -> None:
        text = (KB / "README.md").read_text(encoding="utf-8")
        self.assertIn("village/README.md", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)

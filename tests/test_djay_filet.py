#!/usr/bin/env python3
"""Filet djay : backup sans suppression, refus si djay ouvert, pas de rm."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "_kb" / "outils" / "djay_filet.py"


def load_filet():
    spec = importlib.util.spec_from_file_location("djay_filet", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


filet = load_filet()


class DjayFiletTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name)
        self.library = self.home / "Music" / "djay" / "djay Media Library.djayMediaLibrary"
        self.library.mkdir(parents=True)
        (self.library / "MediaLibrary.db").write_bytes(b"RIFF" + b"\x00" * 120)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_finds_library_under_home(self) -> None:
        found = filet.find_library(self.home)
        self.assertEqual(found, self.library)

    def test_backup_copies_and_keeps_original(self) -> None:
        now = datetime(2026, 8, 19, 23, 0, tzinfo=timezone.utc)
        target = filet.backup_library(self.home, now=now)
        self.assertTrue(target.is_dir())
        self.assertTrue((target / "MediaLibrary.db").is_file())
        self.assertTrue((self.library / "MediaLibrary.db").is_file())
        self.assertEqual(
            (target / "MediaLibrary.db").read_bytes(),
            (self.library / "MediaLibrary.db").read_bytes(),
        )
        self.assertIn("20260819-230000", str(target))

    def test_avant_set_refuses_when_djay_is_open(self) -> None:
        calls: list[list[str]] = []
        code = filet.cmd_avant_set(
            self.home,
            running=True,
            run_defaults=calls.append,
            is_darwin=True,
        )
        self.assertEqual(code, 2)
        self.assertEqual(calls, [])
        backups = list((self.home / "Music" / "djay-backups").glob("**/*"))
        self.assertEqual(backups, [])

    def test_avant_set_backups_and_resets_when_closed(self) -> None:
        calls: list[list[str]] = []
        code = filet.cmd_avant_set(
            self.home,
            running=False,
            run_defaults=calls.append,
            is_darwin=True,
        )
        self.assertEqual(code, 0)
        self.assertEqual(len(calls), 3)
        self.assertTrue((self.library / "MediaLibrary.db").is_file())
        self.assertTrue(any(self.home.joinpath("Music", "djay-backups").rglob("MediaLibrary.db")))
        for argv in calls:
            self.assertNotIn("rm", argv)
            self.assertEqual(argv[0], "defaults")
            self.assertEqual(argv[3], "CMCResetCloudKitState")

    def test_backup_without_library_returns_error(self) -> None:
        empty = self.home / "empty-home"
        empty.mkdir()
        code = filet.cmd_backup(empty)
        self.assertEqual(code, 1)
        self.assertFalse((empty / "Music" / "djay-backups").exists())

    def test_avant_set_writes_etat_and_apres_closes_cycle(self) -> None:
        opens: list[str] = []
        now = datetime(2026, 8, 19, 23, 30, tzinfo=timezone.utc)
        code = filet.cmd_avant_set(
            self.home,
            running=False,
            run_defaults=lambda argv: None,
            is_darwin=True,
            maintenant=now,
            open_settings=lambda: opens.append("icloud"),
        )
        self.assertEqual(code, 0)
        self.assertEqual(opens, ["icloud"])
        etat = filet.read_etat(self.home)
        self.assertIsNotNone(etat)
        self.assertEqual(etat["etat"], "avant")
        self.assertIn("20260819-233000", etat["copie"])
        self.assertEqual(filet.cmd_pendant(self.home), 0)
        self.assertEqual(
            filet.cmd_apres_set(self.home, is_darwin=True, open_settings=lambda: opens.append("after")),
            0,
        )
        etat = filet.read_etat(self.home)
        self.assertEqual(etat["etat"], "apres")
        self.assertTrue(Path(etat["copie"]).exists())
        self.assertEqual(opens, ["icloud", "after"])

    def test_pendant_without_avant_set_fails(self) -> None:
        self.assertEqual(filet.cmd_pendant(self.home), 1)

    def test_cli_status_and_cycle(self) -> None:
        self.assertEqual(filet.main(["status", "--home", str(self.home)]), 0)
        self.assertEqual(filet.main(["avant-set", "--home", str(self.home)]), 0)
        self.assertEqual(filet.main(["pendant", "--home", str(self.home)]), 0)
        self.assertEqual(filet.main(["apres-set", "--home", str(self.home)]), 0)
        self.assertEqual(filet.read_etat(self.home)["etat"], "apres")

    def test_wrapper_stays_in_repo_and_does_not_delete(self) -> None:
        wrapper = ROOT / "_kb" / "outils" / "filet-set.sh"
        text = wrapper.read_text(encoding="utf-8")
        self.assertIn("djay_filet.py", text)
        self.assertNotIn("rm ", text)
        self.assertNotIn("os.remove", text)

    def test_docs_point_to_the_full_cycle(self) -> None:
        filet_set = (ROOT / "_kb" / "outils" / "FILET-SET.md").read_text(encoding="utf-8")
        carte = (ROOT / "_kb" / "liens" / "carte-musique.md").read_text(encoding="utf-8")
        kb_dj = (ROOT / "_kb" / "dj" / "FONCTION.md").read_text(encoding="utf-8")
        self.assertIn("avant-set", filet_set)
        self.assertIn("pendant", filet_set)
        self.assertIn("apres-set", filet_set)
        self.assertIn("FILET-SET.md", carte)
        self.assertIn("FILET-SET.md", kb_dj)

    def test_source_has_no_delete_calls(self) -> None:
        source = MODULE_PATH.read_text(encoding="utf-8")
        self.assertNotIn("os.remove", source)
        self.assertNotIn("shutil.rmtree", source)
        self.assertNotIn("unlink(", source)
        self.assertNotIn("Path.unlink", source)


if __name__ == "__main__":
    unittest.main(verbosity=2)

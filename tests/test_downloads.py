#!/usr/bin/env python3
"""Valide le catalogue, le HTML et les deux voies de téléchargement."""

from __future__ import annotations

import json
import threading
import unittest
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "assets" / "downloads" / "catalog.json"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


def start_server(directory: Path) -> ThreadingHTTPServer:
    handler = partial(QuietHandler, directory=str(directory))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


class DownloadRoutesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = start_server(ROOT)
        host, port = cls.server.server_address
        cls.base = f"http://{host}:{port}"
        with CATALOG_PATH.open(encoding="utf-8") as handle:
            cls.catalog = json.load(handle)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()

    def fetch(self, path: str, method: str = "GET"):
        url = f"{self.base}/{path.lstrip('/')}"
        request = Request(url, method=method)
        try:
            with urlopen(request, timeout=5) as response:
                body = response.read()
                return response.status, response.headers, body
        except HTTPError as error:
            return error.code, error.headers, error.read()

    def test_catalog_lists_existing_files(self) -> None:
        files = self.catalog["files"]
        self.assertGreaterEqual(len(files), 5)
        for item in files:
            path = ROOT / item["path"]
            self.assertTrue(path.is_file(), f"manque {item['path']}")
            self.assertEqual(path.stat().st_size, item["bytes"], item["id"])
            self.assertGreater(item["bytes"], 0)

    def test_direct_http_route_for_each_file(self) -> None:
        for item in self.catalog["files"]:
            status, headers, body = self.fetch(item["path"])
            self.assertEqual(status, 200, item["path"])
            self.assertEqual(len(body), item["bytes"], item["path"])
            content_type = headers.get("Content-Type", "")
            if item["path"].endswith(".wav"):
                self.assertTrue(
                    "audio" in content_type or "octet-stream" in content_type,
                    content_type,
                )
            if item["path"].endswith(".txt"):
                self.assertIn("text/plain", content_type)
            if item["path"].endswith(".json"):
                self.assertIn("json", content_type)

    def test_head_then_get_same_length(self) -> None:
        for item in self.catalog["files"]:
            head_status, head_headers, _ = self.fetch(item["path"], method="HEAD")
            get_status, get_headers, body = self.fetch(item["path"])
            self.assertEqual(head_status, 200, item["path"])
            self.assertEqual(get_status, 200, item["path"])
            self.assertEqual(int(get_headers["Content-Length"]), len(body))
            if "Content-Length" in head_headers:
                self.assertEqual(int(head_headers["Content-Length"]), len(body))

    def test_html_wires_both_download_modes(self) -> None:
        status, _, body = self.fetch("index.html")
        self.assertEqual(status, 200)
        html = body.decode("utf-8")
        self.assertIn('content="width=device-width, initial-scale=1.0"', html)
        self.assertIn('href="index.css"', html)
        self.assertIn('src="index.js"', html)
        self.assertNotIn("script.js", html)
        self.assertNotIn("widt=device-with", html)
        self.assertIn('data-dwet-mode="direct"', html)
        self.assertIn('data-dwet-mode="fetch"', html)
        self.assertGreaterEqual(html.count('aria-label="Télécharger'), 5)
        for item in self.catalog["files"]:
            self.assertIn(item["path"], html)
            if item["section"] in {"prod", "mix", "press"}:
                self.assertIn(f'download="{item["filename"]}"', html)

    def test_fetch_voie_returns_identical_bytes(self) -> None:
        """La voie fetch (GET binaire) doit renvoyer le même fichier que le disque."""
        for item in self.catalog["files"]:
            disk = (ROOT / item["path"]).read_bytes()
            _, _, body = self.fetch(item["path"])
            self.assertEqual(body, disk, item["id"])
            if item["path"].endswith(".wav"):
                self.assertTrue(body.startswith(b"RIFF"), item["id"])
                self.assertIn(b"WAVE", body[:16])

    def test_static_assets_are_non_empty(self) -> None:
        for relative in ("index.css", "index.js", "assets/icons/favicon.svg"):
            status, _, body = self.fetch(relative)
            self.assertEqual(status, 200, relative)
            self.assertGreater(len(body), 200, relative)

    def test_missing_file_is_404(self) -> None:
        status, _, _ = self.fetch("assets/downloads/prod/does-not-exist.wav")
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)

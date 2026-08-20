#!/usr/bin/env python3
"""Filet set djay : sauvegarder la bibliothèque, reset CloudKit. Ne supprime rien."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path


BUNDLE_IDS = (
    "com.algoriddim.djay-iphone-free",
    "com.algoriddim.djay-pro",
    "com.algoriddim.djay",
)

DJAY_PROCESS_NAMES = ("djay Pro", "djay")
ICLOUD_SETTINGS = "x-apple.systempreferences:com.apple.preferences.AppleIDPrefPane"
SCRIPT_PATH = Path(__file__).resolve()


def nfc(path: Path) -> Path:
    return Path(unicodedata.normalize("NFC", str(path)))


def default_library(home: Path) -> Path:
    return nfc(home / "Music" / "djay" / "djay Media Library.djayMediaLibrary")


def backup_root(home: Path) -> Path:
    return nfc(home / "Music" / "djay-backups")


def etat_path(home: Path) -> Path:
    return backup_root(home) / "filet-etat.txt"


def find_library(home: Path) -> Path | None:
    candidate = default_library(home)
    if candidate.exists():
        return candidate
    folder = nfc(home / "Music" / "djay")
    if not folder.is_dir():
        return None
    matches = [
        nfc(path)
        for path in folder.iterdir()
        if path.name.endswith(".djayMediaLibrary")
    ]
    return matches[0] if len(matches) == 1 else None


def library_bytes(path: Path) -> int:
    if path.is_file():
        return path.stat().st_size
    total = 0
    for child in path.rglob("*"):
        if child.is_file():
            total += child.stat().st_size
    return total


def format_size(num: int) -> str:
    if num < 1024:
        return f"{num} o"
    if num < 1024 * 1024:
        return f"{num / 1024:.1f} Ko"
    if num < 1024 * 1024 * 1024:
        return f"{num / (1024 * 1024):.1f} Mo"
    return f"{num / (1024 * 1024 * 1024):.2f} Go"


def djay_is_running(process_names: tuple[str, ...] = DJAY_PROCESS_NAMES) -> bool:
    for name in process_names:
        result = subprocess.run(
            ["pgrep", "-x", name],
            check=False,
            capture_output=True,
        )
        if result.returncode == 0:
            return True
    return False


def copy_library(source: Path, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError(f"déjà là : {destination}")
    if source.is_dir():
        shutil.copytree(source, destination)
    else:
        shutil.copy2(source, destination)
    return destination


def backup_library(home: Path, now: datetime | None = None) -> Path:
    source = find_library(home)
    if source is None:
        raise FileNotFoundError("bibliothèque djay introuvable dans Music/djay")
    stamp = (now or datetime.now(timezone.utc)).strftime("%Y%m%d-%H%M%S")
    target = backup_root(home) / stamp / source.name
    return copy_library(source, target)


def write_etat(home: Path, etat: str, copie: str = "", maintenant: datetime | None = None) -> Path:
    path = etat_path(home)
    path.parent.mkdir(parents=True, exist_ok=True)
    stamp = (maintenant or datetime.now(timezone.utc)).isoformat()
    previous = read_etat(home) or {}
    copie_line = copie or previous.get("copie", "")
    path.write_text(
        f"etat={etat}\ndepuis={stamp}\ncopie={copie_line}\n",
        encoding="utf-8",
    )
    return path


def read_etat(home: Path) -> dict[str, str] | None:
    path = etat_path(home)
    if not path.is_file():
        return None
    data: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        data[key.strip()] = value.strip()
    return data or None


def reset_cloudkit(run_defaults) -> list[str]:
    written = []
    for bundle in BUNDLE_IDS:
        run_defaults(
            ["defaults", "write", bundle, "CMCResetCloudKitState", "-bool", "true"]
        )
        written.append(bundle)
    return written


def darwin_defaults(argv: list[str]) -> None:
    subprocess.run(argv, check=True)


def darwin_open_icloud() -> None:
    subprocess.run(["open", ICLOUD_SETTINGS], check=False)


def remind_icloud_off() -> str:
    return (
        "Avant le set : Réglages Mac → Apple ID → iCloud → djay → OFF.\n"
        "La sync, c’est après. Pas pendant."
    )


def remind_icloud_pendant() -> str:
    return (
        "Pendant le set : iCloud djay reste OFF. Pas de sync. Pas de reset.\n"
        "Tu joues. Le filet tient tout seul."
    )


def remind_icloud_on() -> str:
    return (
        "Après le set : Réglages Mac → Apple ID → iCloud → djay → ON.\n"
        "La bibliothèque se sync au calme, djay fermé ou ouvert hors live."
    )


def cmd_status(home: Path, running: bool) -> int:
    library = find_library(home)
    print(f"script : {SCRIPT_PATH}")
    print(f"maison : {home}")
    etat = read_etat(home)
    if etat:
        print(f"filet : {etat.get('etat', '?')} depuis {etat.get('depuis', '?')}")
        if etat.get("copie"):
            print(f"dernière copie : {etat['copie']}")
    else:
        print("filet : aucun (pas encore d’avant-set)")
    if library is None:
        print("bibliothèque : introuvable (Music/djay)")
        return 1
    size = library_bytes(library)
    print(f"bibliothèque : {library}")
    print(f"taille : {format_size(size)}")
    if size >= 200 * 1024 * 1024:
        print("alerte : fichier gros — CloudKit a probablement gonflé la base")
    print(f"djay ouvert : {'oui — quitte-le avant le filet' if running else 'non'}")
    current = (etat or {}).get("etat")
    if current == "avant":
        print(remind_icloud_pendant())
    elif current == "apres":
        print(remind_icloud_on())
    else:
        print(remind_icloud_off())
    return 0


def cmd_backup(home: Path, maintenant: datetime | None = None) -> int:
    try:
        target = backup_library(home, now=maintenant)
    except FileNotFoundError as error:
        print(error)
        return 1
    print(f"copie : {target}")
    print(f"taille : {format_size(library_bytes(target))}")
    print("l’original n’a pas été touché")
    return 0


def cmd_avant_set(
    home: Path,
    running: bool,
    run_defaults,
    is_darwin: bool,
    maintenant: datetime | None = None,
    open_settings=None,
) -> int:
    if running:
        print("djay est ouvert. Ferme-le, puis relance avant-set.")
        return 2
    try:
        target = backup_library(home, now=maintenant)
    except FileNotFoundError as error:
        print(error)
        return 1
    print(f"copie : {target}")
    print(f"taille : {format_size(library_bytes(target))}")
    print("l’original n’a pas été touché")
    write_etat(home, "avant", copie=str(target), maintenant=maintenant)
    if is_darwin:
        reset_cloudkit(run_defaults)
        print("CloudKit : reset demandé (officiel Algoriddim)")
        if open_settings:
            open_settings()
            print("Réglages iCloud ouverts → décoche djay")
    else:
        print("CloudKit : à lancer sur le Mac (pas ici)")
    print(remind_icloud_off())
    return 0


def cmd_pendant(home: Path) -> int:
    etat = read_etat(home)
    if etat and etat.get("etat") != "avant":
        print("filet pas en avant-set. Lance avant-set avant de jouer.")
        return 1
    if not etat:
        print("pas d’avant-set encore. Lance avant-set, iCloud OFF, puis joue.")
        return 1
    print(remind_icloud_pendant())
    return 0


def cmd_apres_set(home: Path, is_darwin: bool, open_settings=None) -> int:
    etat = read_etat(home)
    if etat and etat.get("copie"):
        print(f"copie gardée : {etat['copie']}")
    write_etat(home, "apres", maintenant=datetime.now(timezone.utc))
    print(remind_icloud_on())
    if is_darwin and open_settings:
        open_settings()
        print("Réglages iCloud ouverts → recoche djay")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Filet set djay : backup + reset CloudKit. Ne supprime rien."
    )
    parser.add_argument(
        "action",
        choices=("status", "backup", "avant-set", "pendant", "apres-set"),
        help="status, backup, avant-set, pendant, apres-set",
    )
    parser.add_argument(
        "--home",
        type=Path,
        default=None,
        help="maison à utiliser (tests). Défaut : dossier utilisateur.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    home = nfc((args.home or Path.home()).expanduser())
    running = djay_is_running()
    is_darwin = sys.platform == "darwin"
    opener = darwin_open_icloud if is_darwin else None
    if args.action == "status":
        return cmd_status(home, running)
    if args.action == "backup":
        return cmd_backup(home)
    if args.action == "avant-set":
        return cmd_avant_set(
            home,
            running,
            darwin_defaults if is_darwin else (lambda argv: None),
            is_darwin,
            open_settings=opener,
        )
    if args.action == "pendant":
        return cmd_pendant(home)
    return cmd_apres_set(home, is_darwin, open_settings=opener)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Rename images in a folder to YYYYMMDD-HHMMSS based on capture date.

Date sources (first match wins):
1. EXIF DateTimeOriginal / DateTimeDigitized / DateTime
2. Android-style filename: IMGYYYYMMDDHHMMSS...

Usage:
  # Preview only (safe)
  python3 scripts/rename-images-by-date.py public/images/markus/gallery

  # Actually rename
  python3 scripts/rename-images-by-date.py public/images/markus/gallery --apply
"""

from __future__ import annotations

import argparse
import re
import struct
import sys
from pathlib import Path

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}


def exif_datetime(path: Path) -> str | None:
    data = path.read_bytes()
    if data[:2] != b"\xff\xd8":
        return None

    i = 2
    while i < len(data) - 4:
        if data[i] != 0xFF:
            i += 1
            continue

        marker = data[i + 1]
        if marker in (0xD9, 0xDA):
            break

        seglen = struct.unpack(">H", data[i + 2 : i + 4])[0]
        if marker == 0xE1 and data[i + 4 : i + 8] == b"Exif":
            tiff = i + 10
            endian = data[tiff : tiff + 2]
            endian_fmt = "<" if endian == b"II" else ">"
            ifd0 = tiff + struct.unpack(endian_fmt + "I", data[tiff + 4 : tiff + 8])[0]

            def read_ifd(offset: int) -> dict[int, object]:
                entries = struct.unpack(endian_fmt + "H", data[offset : offset + 2])[0]
                tags: dict[int, object] = {}
                for e in range(entries):
                    entry = offset + 2 + e * 12
                    tag, typ, count = struct.unpack(
                        endian_fmt + "HHI", data[entry : entry + 8]
                    )
                    val_or_off = data[entry + 8 : entry + 12]
                    if typ == 2:
                        if count <= 4:
                            val = (
                                val_or_off[:count]
                                .split(b"\x00")[0]
                                .decode("ascii", "ignore")
                            )
                        else:
                            off = struct.unpack(endian_fmt + "I", val_or_off)[0]
                            start = tiff + off
                            val = (
                                data[start : start + count]
                                .split(b"\x00")[0]
                                .decode("ascii", "ignore")
                            )
                        tags[tag] = val
                    elif typ == 4 and count == 1:
                        tags[tag] = struct.unpack(endian_fmt + "I", val_or_off)[0]
                return tags

            ifd0_tags = read_ifd(ifd0)
            if 0x8769 in ifd0_tags:
                exif_off = ifd0_tags[0x8769]
                if isinstance(exif_off, int):
                    exif = read_ifd(tiff + exif_off)
                    for key in (0x9003, 0x9004):
                        value = exif.get(key)
                        if isinstance(value, str) and value:
                            return value
            datetime_tag = ifd0_tags.get(0x0132)
            if isinstance(datetime_tag, str) and datetime_tag:
                return datetime_tag
            return None

        i += 2 + seglen

    return None


def from_android_name(name: str) -> str | None:
    match = re.match(r"^IMG(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})", name, re.I)
    if not match:
        return None
    year, month, day, hour, minute, second = match.groups()
    return f"{year}:{month}:{day} {hour}:{minute}:{second}"


def to_stamp(dt: str) -> str | None:
    match = re.match(
        r"^(\d{4}):(\d{2}):(\d{2})[ T](\d{2}):(\d{2}):(\d{2})",
        dt,
    )
    if not match:
        return None
    year, month, day, hour, minute, second = match.groups()
    return f"{year}{month}{day}-{hour}{minute}{second}"


def normalize_ext(suffix: str) -> str:
    ext = suffix.lower()
    return ".jpg" if ext == ".jpeg" else ext


def plan_renames(folder: Path) -> tuple[list[tuple[Path, Path, str]], list[str]]:
    files = sorted(
        p
        for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXT and p.name != ".gitkeep"
    )

    planned: list[tuple[Path, str, str]] = []
    missing: list[str] = []

    for path in files:
        dt = exif_datetime(path) or from_android_name(path.name)
        stamp = to_stamp(dt) if dt else None
        if not stamp or not dt:
            missing.append(path.name)
            continue
        planned.append((path, f"{stamp}{normalize_ext(path.suffix)}", dt))

    used: set[str] = set()
    result: list[tuple[Path, Path, str]] = []

    for path, new_name, dt in planned:
        base = Path(new_name).stem
        ext = Path(new_name).suffix
        candidate = new_name
        n = 2

        while True:
            key = candidate.lower()
            target = folder / candidate
            conflict = key in used or (target.exists() and target.resolve() != path.resolve())
            if not conflict:
                break
            candidate = f"{base}-{n}{ext}"
            n += 1

        used.add(candidate.lower())
        result.append((path, folder / candidate, dt))

    return result, missing


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rename images to YYYYMMDD-HHMMSS using EXIF/capture date."
    )
    parser.add_argument(
        "folder",
        type=Path,
        help="Folder with images, e.g. public/images/markus/gallery",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually rename files. Without this flag, only prints a dry-run.",
    )
    args = parser.parse_args()

    folder = args.folder.expanduser().resolve()
    if not folder.is_dir():
        print(f"Error: folder not found: {folder}", file=sys.stderr)
        return 1

    planned, missing = plan_renames(folder)

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"=== {mode}: {folder} ===")

    changed = 0
    for src, dest, dt in planned:
        if src.resolve() == dest.resolve():
            print(f"{src.name}  (already correct)  [{dt}]")
            continue
        print(f"{src.name}  ->  {dest.name}  [{dt}]")
        if args.apply:
            src.rename(dest)
        changed += 1

    if missing:
        print("\n=== Missing date (skipped) ===")
        for name in missing:
            print(name)

    print(
        f"\n{changed} file(s) {'renamed' if args.apply else 'would be renamed'}, "
        f"{len(missing)} skipped."
    )
    if not args.apply and changed:
        print("Re-run with --apply to perform renames.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

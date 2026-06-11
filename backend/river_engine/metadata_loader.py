from __future__ import annotations

import json
import re
from pathlib import Path

import cv2
import numpy as np

from river_engine.config import LETTERS_DIR, METADATA_DIR, PROJECT_ROOT
from river_engine.geometry import to_points
from river_engine.types import GlyphRecord


def _resolve_image_path(raw: str) -> Path:
    cleaned = raw.replace("\\", "/")
    if cleaned.startswith("assets/"):
        return PROJECT_ROOT / cleaned
    candidate = PROJECT_ROOT / cleaned
    if candidate.exists():
        return candidate
    name = Path(cleaned).name
    for hit in LETTERS_DIR.rglob(name):
        return hit
    return PROJECT_ROOT / cleaned


def _letter_key(letter: str) -> str:
    return letter.lower()


def _folder_for_letter(letter: str) -> Path | None:
    key = _letter_key(letter)
    for child in METADATA_DIR.iterdir():
        if child.is_dir() and child.name.lower() == key:
            return child
    return None


def validate_metadata(meta: dict, image_path: Path) -> list[str]:
    errors: list[str] = []
    if not image_path.exists():
        errors.append(f"missing image: {image_path}")
    for field in (
        "entry_point",
        "exit_point",
        "entry_angle",
        "exit_angle",
        "letter_points",
        "river_points",
    ):
        if field not in meta:
            errors.append(f"missing field: {field}")
    if "letter_points" in meta and len(meta["letter_points"]) < 2:
        errors.append("letter_points too short")
    if "river_points" in meta and len(meta["river_points"]) < 2:
        errors.append("river_points too short")
    entry = meta.get("entry_point")
    exit_p = meta.get("exit_point")
    if entry and exit_p and np.allclose(entry, exit_p):
        errors.append("entry and exit are identical")
    return errors


def load_glyph_from_metadata(meta_path: Path) -> GlyphRecord | None:
    with meta_path.open("r", encoding="utf-8") as handle:
        meta = json.load(handle)

    image_path = _resolve_image_path(meta["image"])
    errors = validate_metadata(meta, image_path)
    if errors:
        return None

    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        return None

    letter = str(meta.get("letter", meta_path.parent.name))
    letter_points = to_points(meta["letter_points"])
    river_points = to_points(meta["river_points"])
    entry = to_points([meta["entry_point"]])[0]
    exit_p = to_points([meta["exit_point"]])[0]

    letter_bbox = tuple(meta.get("letter_bbox", meta.get("crop_safe_region", (0, 0, image.shape[1], image.shape[0]))))
    river_bbox = tuple(meta.get("river_bbox", letter_bbox))

    return GlyphRecord(
        letter=letter,
        image_path=str(image_path),
        metadata=meta,
        image=image,
        letter_points=letter_points,
        river_points=river_points,
        entry_point=entry,
        exit_point=exit_p,
        entry_angle=float(meta["entry_angle"]),
        exit_angle=float(meta["exit_angle"]),
        average_width=float(meta.get("average_width", meta.get("letter_width", 12.0))),
        letter_width=float(meta.get("letter_width", meta.get("average_width", 12.0))),
        letter_bbox=(int(letter_bbox[0]), int(letter_bbox[1]), int(letter_bbox[2]), int(letter_bbox[3])),
        river_bbox=(int(river_bbox[0]), int(river_bbox[1]), int(river_bbox[2]), int(river_bbox[3])),
        connection_strength=float(meta.get("connection_strength", 1.0)),
    )


def load_letter_candidates(letter: str) -> list[GlyphRecord]:
    folder = _folder_for_letter(letter)
    if folder is None:
        return []

    glyphs: list[GlyphRecord] = []
    for meta_path in sorted(folder.glob("*.json")):
        glyph = load_glyph_from_metadata(meta_path)
        if glyph is not None:
            glyphs.append(glyph)
    return glyphs


def index_all_metadata() -> dict[str, list[GlyphRecord]]:
    catalog: dict[str, list[GlyphRecord]] = {}
    if not METADATA_DIR.exists():
        return catalog

    for folder in METADATA_DIR.iterdir():
        if not folder.is_dir():
            continue
        letter = folder.name
        if not re.fullmatch(r"[A-Za-z]", letter):
            continue
        glyphs = load_letter_candidates(letter)
        if glyphs:
            catalog[_letter_key(letter)] = glyphs
    return catalog

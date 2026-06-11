from __future__ import annotations

import copy
import math

import cv2
import numpy as np

from river_engine.config import (
    LETTER_SAFE_PAD,
    MAX_TILT_DEG,
    TARGET_RIVER_WIDTH,
)
from river_engine.geometry import (
    apply_affine_to_points,
    bbox_from_points,
    clamp_bbox,
    rotate_image,
)
from river_engine.types import GlyphRecord


def _flow_rotation(glyph: GlyphRecord) -> float:
    entry = glyph.entry_point
    exit_p = glyph.exit_point
    dx = exit_p[0] - entry[0]
    dy = exit_p[1] - entry[1]
    current = math.degrees(math.atan2(-dy, dx))
    return -current


def _clamp_tilt(rotation_deg: float) -> float:
    return float(np.clip(rotation_deg, -MAX_TILT_DEG, MAX_TILT_DEG))


def _flip_horizontal(glyph: GlyphRecord) -> GlyphRecord:
    h, w = glyph.image.shape[:2]
    flipped = cv2.flip(glyph.image, 1)

    def flip_x(pts: np.ndarray) -> np.ndarray:
        out = pts.copy()
        out[:, 0] = (w - 1) - out[:, 0]
        return out

    def flip_angle(angle: float) -> float:
        return 180.0 - angle

    lb = glyph.letter_bbox
    rb = glyph.river_bbox
    return GlyphRecord(
        letter=glyph.letter,
        image_path=glyph.image_path,
        metadata=glyph.metadata,
        image=flipped,
        letter_points=flip_x(glyph.letter_points),
        river_points=flip_x(glyph.river_points),
        entry_point=flip_x(glyph.entry_point[None])[0],
        exit_point=flip_x(glyph.exit_point[None])[0],
        entry_angle=flip_angle(glyph.entry_angle),
        exit_angle=flip_angle(glyph.exit_angle),
        average_width=glyph.average_width,
        letter_width=glyph.letter_width,
        letter_bbox=(w - lb[2], lb[1], w - lb[0], lb[3]),
        river_bbox=(w - rb[2], rb[1], w - rb[0], rb[3]),
        connection_strength=glyph.connection_strength,
        scale=glyph.scale,
        rotation_deg=glyph.rotation_deg,
        offset=glyph.offset,
        crop_box=glyph.crop_box,
    )


def _content_bounds(glyph: GlyphRecord) -> tuple[int, int, int, int]:
    """Crop box that keeps letter, river, and connection endpoints intact."""
    chunks: list[np.ndarray] = []
    if len(glyph.letter_points) > 0:
        chunks.append(glyph.letter_points)
    if len(glyph.river_points) > 0:
        chunks.append(glyph.river_points)
    chunks.append(glyph.entry_point.reshape(1, 2))
    chunks.append(glyph.exit_point.reshape(1, 2))
    pts = np.vstack(chunks)
    pad = max(LETTER_SAFE_PAD + 6, int(round(glyph.average_width * 2.4)))
    return bbox_from_points(pts, pad=pad)


def _crop_glyph(glyph: GlyphRecord) -> GlyphRecord:
    h, w = glyph.image.shape[:2]
    x0, y0, x1, y1 = _content_bounds(glyph)
    x0, y0, x1, y1 = clamp_bbox((x0, y0, x1, y1), w, h)

    cropped = glyph.image[y0:y1, x0:x1].copy()
    shift = np.array([x0, y0], dtype=np.float64)

    def shift_pts(pts: np.ndarray) -> np.ndarray:
        return pts - shift

    lb = glyph.letter_bbox
    rb = glyph.river_bbox
    return GlyphRecord(
        letter=glyph.letter,
        image_path=glyph.image_path,
        metadata=glyph.metadata,
        image=cropped,
        letter_points=shift_pts(glyph.letter_points),
        river_points=shift_pts(glyph.river_points),
        entry_point=glyph.entry_point - shift,
        exit_point=glyph.exit_point - shift,
        entry_angle=glyph.entry_angle,
        exit_angle=glyph.exit_angle,
        average_width=glyph.average_width,
        letter_width=glyph.letter_width,
        letter_bbox=(lb[0] - x0, lb[1] - y0, lb[2] - x0, lb[3] - y0),
        river_bbox=(rb[0] - x0, rb[1] - y0, rb[2] - x0, rb[3] - y0),
        connection_strength=glyph.connection_strength,
        crop_box=(x0, y0, x1, y1),
    )


def _scale_glyph(glyph: GlyphRecord, scale: float) -> GlyphRecord:
    if abs(scale - 1.0) < 1e-4:
        return glyph
    h, w = glyph.image.shape[:2]
    new_w = max(8, int(round(w * scale)))
    new_h = max(8, int(round(h * scale)))
    resized = cv2.resize(glyph.image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    def scale_pts(pts: np.ndarray) -> np.ndarray:
        return pts * scale

    lb = glyph.letter_bbox
    rb = glyph.river_bbox
    return GlyphRecord(
        letter=glyph.letter,
        image_path=glyph.image_path,
        metadata=glyph.metadata,
        image=resized,
        letter_points=scale_pts(glyph.letter_points),
        river_points=scale_pts(glyph.river_points),
        entry_point=scale_pts(glyph.entry_point[None])[0],
        exit_point=scale_pts(glyph.exit_point[None])[0],
        entry_angle=glyph.entry_angle,
        exit_angle=glyph.exit_angle,
        average_width=glyph.average_width * scale,
        letter_width=glyph.letter_width * scale,
        letter_bbox=(
            int(lb[0] * scale),
            int(lb[1] * scale),
            int(lb[2] * scale),
            int(lb[3] * scale),
        ),
        river_bbox=(
            int(rb[0] * scale),
            int(rb[1] * scale),
            int(rb[2] * scale),
            int(rb[3] * scale),
        ),
        connection_strength=glyph.connection_strength,
        scale=glyph.scale * scale,
        rotation_deg=glyph.rotation_deg,
        offset=glyph.offset,
        crop_box=glyph.crop_box,
    )


def _rotate_glyph(glyph: GlyphRecord, rotation_deg: float) -> GlyphRecord:
    if abs(rotation_deg) < 1e-4:
        return glyph
    h, w = glyph.image.shape[:2]
    center = (w / 2.0, h / 2.0)
    rotated, matrix = rotate_image(glyph.image, rotation_deg, center=center)

    def rot_pts(pts: np.ndarray) -> np.ndarray:
        return apply_affine_to_points(pts, matrix)

    lb = glyph.letter_bbox
    rb = glyph.river_bbox

    def rot_box(box):
        pts = np.array(
            [
                [box[0], box[1]],
                [box[2], box[1]],
                [box[2], box[3]],
                [box[0], box[3]],
            ],
            dtype=np.float64,
        )
        r = rot_pts(pts)
        return (
            int(r[:, 0].min()),
            int(r[:, 1].min()),
            int(r[:, 0].max()),
            int(r[:, 1].max()),
        )

    return GlyphRecord(
        letter=glyph.letter,
        image_path=glyph.image_path,
        metadata=glyph.metadata,
        image=rotated,
        letter_points=rot_pts(glyph.letter_points),
        river_points=rot_pts(glyph.river_points),
        entry_point=rot_pts(glyph.entry_point[None])[0],
        exit_point=rot_pts(glyph.exit_point[None])[0],
        entry_angle=glyph.entry_angle + rotation_deg,
        exit_angle=glyph.exit_angle + rotation_deg,
        average_width=glyph.average_width,
        letter_width=glyph.letter_width,
        letter_bbox=rot_box(lb),
        river_bbox=rot_box(rb),
        connection_strength=glyph.connection_strength,
        scale=glyph.scale,
        rotation_deg=glyph.rotation_deg + rotation_deg,
        offset=glyph.offset,
        crop_box=glyph.crop_box,
    )


def normalize_glyph(glyph: GlyphRecord, target_width: float = TARGET_RIVER_WIDTH) -> GlyphRecord:
    g = copy.deepcopy(glyph)

    width_scale = target_width / max(g.average_width, 1.0)
    width_scale = float(np.clip(width_scale, 0.55, 1.8))
    g = _scale_glyph(g, width_scale)

    entry = g.entry_point
    exit_p = g.exit_point
    if exit_p[0] < entry[0]:
        g = _flip_horizontal(g)

    tilt = _clamp_tilt(_flow_rotation(g))
    if abs(tilt) > 0.05:
        g = _rotate_glyph(g, tilt)
        g = _crop_glyph(g)

    g = _crop_glyph(g)
    return g


def normalize_candidates(candidates: list[GlyphRecord]) -> list[GlyphRecord]:
    return [normalize_glyph(g) for g in candidates]

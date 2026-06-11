from __future__ import annotations

import cv2
import numpy as np

from river_engine.geometry import unit_from_angle
from river_engine.types import PlacedGlyph


def draw_debug_overlay(
    canvas: np.ndarray,
    placed: list[PlacedGlyph],
) -> np.ndarray:
    overlay = canvas.copy()
    for item in placed:
        g = item.glyph
        offset = np.array([item.x, item.y], dtype=np.float64)

        letter_pts = (g.letter_points + offset).astype(np.int32)
        river_pts = (g.river_points + offset).astype(np.int32)
        if len(letter_pts) > 1:
            cv2.polylines(overlay, [letter_pts], False, (0, 255, 255), 2)
        if len(river_pts) > 1:
            cv2.polylines(overlay, [river_pts], False, (255, 120, 0), 2)

        entry = (g.entry_point + offset).astype(int)
        exit_p = (g.exit_point + offset).astype(int)
        cv2.circle(overlay, tuple(entry), 6, (0, 255, 0), -1)
        cv2.circle(overlay, tuple(exit_p), 6, (0, 0, 255), -1)

        e_dir = unit_from_angle(g.entry_angle) * 28
        x_dir = unit_from_angle(g.exit_angle) * 28
        cv2.arrowedLine(
            overlay,
            tuple(entry),
            tuple((entry + e_dir).astype(int)),
            (0, 255, 0),
            2,
            tipLength=0.25,
        )
        cv2.arrowedLine(
            overlay,
            tuple(exit_p),
            tuple((exit_p + x_dir).astype(int)),
            (0, 0, 255),
            2,
            tipLength=0.25,
        )

        lb = g.letter_bbox
        cv2.rectangle(
            overlay,
            (int(lb[0] + item.x), int(lb[1] + item.y)),
            (int(lb[2] + item.x), int(lb[3] + item.y)),
            (255, 0, 255),
            1,
        )

        if item.bridge_before is not None and item.bridge_mask is not None:
            bx, by = item.bridge_offset
            mask = item.bridge_mask
            tint = np.zeros_like(item.bridge_before)
            tint[:, :] = (80, 180, 255)
            region = overlay[by : by + mask.shape[0], bx : bx + mask.shape[1]]
            alpha = (mask.astype(np.float32) / 255.0)[..., None]
            if region.shape[:2] == alpha.shape[:2]:
                blended = region * (1 - alpha * 0.45) + tint * alpha * 0.45
                overlay[by : by + mask.shape[0], bx : bx + mask.shape[1]] = blended.astype(np.uint8)

    return overlay

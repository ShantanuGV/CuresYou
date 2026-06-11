from __future__ import annotations

import random
from pathlib import Path

import cv2
import numpy as np

from river_engine.config import RIVER_TILE_DIR
from river_engine.geometry import bezier_curve, resample_polyline, unit_from_angle


class RibbonTextureSource:
    """Samples real satellite river tiles for bridge texture (ribbon is too large to decode)."""

    def __init__(self, tile_dir: Path = RIVER_TILE_DIR):
        self.tile_dir = tile_dir
        self._tiles: list[np.ndarray] = []
        self._load_tiles()

    def _load_tiles(self, limit: int = 160) -> None:
        if not self.tile_dir.exists():
            return
        paths = sorted(self.tile_dir.glob("tile_*.jpg"))[:limit]
        for path in paths:
            tile = cv2.imread(str(path), cv2.IMREAD_COLOR)
            if tile is not None and tile.size > 0:
                self._tiles.append(tile)

    def sample_patch(self, width: int, height: int, seed: int = 0) -> np.ndarray:
        width = max(8, width)
        height = max(8, height)
        rng = random.Random(seed)

        if not self._tiles:
            return np.full((height, width, 3), (72, 88, 54), dtype=np.uint8)

        tile = self._tiles[rng.randrange(len(self._tiles))]
        th, tw = tile.shape[:2]
        if tw >= width and th >= height:
            x = rng.randint(0, tw - width)
            y = rng.randint(0, th - height)
            return tile[y : y + height, x : x + width].copy()
        return cv2.resize(tile, (width, height), interpolation=cv2.INTER_AREA)

    def sample_along_path(
        self,
        centerline: np.ndarray,
        strip_width: int,
        seed: int = 0,
    ) -> tuple[np.ndarray, np.ndarray]:
        if len(centerline) < 2:
            return np.zeros((1, 1, 3), dtype=np.uint8), np.zeros((1, 1), dtype=np.uint8)

        pts = resample_polyline(centerline, max(16, len(centerline)))
        lengths = np.linalg.norm(np.diff(pts, axis=0), axis=1)
        total_len = max(4, int(np.sum(lengths)))
        patch_h = strip_width * 3
        patch_w = total_len + strip_width * 2
        patch = self.sample_patch(patch_w, patch_h, seed=seed)

        canvas = np.zeros((patch_h, patch_w, 3), dtype=np.uint8)
        mask = np.zeros((patch_h, patch_w), dtype=np.uint8)
        cursor = strip_width

        for i in range(len(pts) - 1):
            p0 = pts[i]
            p1 = pts[i + 1]
            seg_len = max(1, int(np.linalg.norm(p1 - p0)))
            direction = p1 - p0
            angle = np.degrees(np.arctan2(-direction[1], direction[0]))
            x_end = min(patch_w, cursor + seg_len)
            strip = patch[:, cursor:x_end]
            if strip.size == 0:
                continue
            rotated = self._rotate_strip(strip, angle)
            rh, rw = rotated.shape[:2]
            cx = cursor + seg_len // 2
            cy = patch_h // 2
            x0 = max(0, cx - rw // 2)
            y0 = max(0, cy - rh // 2)
            x1 = min(patch_w, x0 + rw)
            y1 = min(patch_h, y0 + rh)
            src = rotated[: y1 - y0, : x1 - x0]
            if src.size == 0:
                continue
            canvas[y0:y1, x0:x1] = src
            mask[y0:y1, x0:x1] = 255
            cursor += seg_len

        return canvas, mask

    @staticmethod
    def _rotate_strip(strip: np.ndarray, angle_deg: float) -> np.ndarray:
        h, w = strip.shape[:2]
        matrix = cv2.getRotationMatrix2D((w / 2, h / 2), angle_deg, 1.0)
        return cv2.warpAffine(
            strip,
            matrix,
            (w, h),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REFLECT101,
        )


def build_bridge_centerline(
    start: np.ndarray,
    end: np.ndarray,
    start_angle: float,
    end_angle: float,
    samples: int = 48,
) -> np.ndarray:
    dist = float(np.linalg.norm(end - start))
    offset = max(20.0, dist * 0.35)
    p0 = start.astype(np.float64)
    p3 = end.astype(np.float64)
    p1 = p0 + unit_from_angle(start_angle) * offset
    p2 = p3 - unit_from_angle(end_angle) * offset
    return bezier_curve(p0, p1, p2, p3, samples=samples)

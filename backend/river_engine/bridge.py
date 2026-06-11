from __future__ import annotations

import numpy as np

from river_engine.blending import build_river_mask
from river_engine.config import BRIDGE_GAP_THRESHOLD
from river_engine.geometry import path_length
from river_engine.ribbon import RibbonTextureSource, build_bridge_centerline


class BridgeBuilder:
    def __init__(self, texture: RibbonTextureSource | None = None):
        self.texture = texture or RibbonTextureSource()

    def needs_bridge(
        self,
        exit_point: np.ndarray,
        entry_point: np.ndarray,
        angle_diff: float,
        gap_threshold: float = BRIDGE_GAP_THRESHOLD,
    ) -> bool:
        gap = float(np.linalg.norm(entry_point - exit_point))
        return gap > gap_threshold or angle_diff > 28.0

    def build(
        self,
        exit_point: np.ndarray,
        entry_point: np.ndarray,
        exit_angle: float,
        entry_angle: float,
        river_width: float,
        seed: int = 0,
    ) -> tuple[np.ndarray, np.ndarray, tuple[int, int]]:
        centerline = build_bridge_centerline(
            exit_point,
            entry_point,
            exit_angle,
            entry_angle,
        )
        strip_w = max(8, int(round(river_width * 1.4)))
        patch, _ = self.texture.sample_along_path(centerline, strip_w, seed=seed)

        local_pts = centerline - centerline.min(axis=0)
        local_pts[:, 0] -= centerline[:, 0].min()
        local_pts[:, 1] -= centerline[:, 1].min()

        h, w = patch.shape[:2]
        mask = build_river_mask(
            local_pts + np.array([strip_w, strip_w]),
            (h, w),
            int(round(river_width)),
        )
        offset = (
            int(centerline[:, 0].min() - strip_w),
            int(centerline[:, 1].min() - strip_w),
        )
        gap = path_length(centerline)
        if gap < 8:
            return np.zeros((1, 1, 3), dtype=np.uint8), np.zeros((1, 1), dtype=np.uint8), (0, 0)
        return patch, mask, offset

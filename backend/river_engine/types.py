from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class GlyphRecord:
    letter: str
    image_path: str
    metadata: dict[str, Any]
    image: np.ndarray
    letter_points: np.ndarray
    river_points: np.ndarray
    entry_point: np.ndarray
    exit_point: np.ndarray
    entry_angle: float
    exit_angle: float
    average_width: float
    letter_width: float
    letter_bbox: tuple[int, int, int, int]
    river_bbox: tuple[int, int, int, int]
    connection_strength: float = 1.0
    scale: float = 1.0
    rotation_deg: float = 0.0
    offset: tuple[float, float] = (0.0, 0.0)
    crop_box: tuple[int, int, int, int] = (0, 0, 0, 0)

    @property
    def height(self) -> int:
        return self.image.shape[0]

    @property
    def width(self) -> int:
        return self.image.shape[1]


@dataclass
class PlacedGlyph:
    glyph: GlyphRecord
    x: int
    y: int
    index: int = 0
    blend_mode: str = "over"
    z_order: int = 0
    bridge_before: np.ndarray | None = None
    bridge_mask: np.ndarray | None = None
    bridge_offset: tuple[int, int] = (0, 0)


@dataclass
class CompositionResult:
    canvas: np.ndarray
    placed: list[PlacedGlyph]
    score: float
    word: str

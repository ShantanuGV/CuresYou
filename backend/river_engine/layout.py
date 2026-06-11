from __future__ import annotations

import random

import numpy as np

from river_engine.config import JUNCTION_OVERLAP_FACTOR, LAYOUT_RANDOM_SEED
from river_engine.types import GlyphRecord, PlacedGlyph

_JUNCTION_MODES = ("connect", "over", "under")
_rng = random.Random(LAYOUT_RANDOM_SEED)


def river_flow_y(glyph: GlyphRecord, y_offset: int = 0) -> float:
    return y_offset + 0.5 * (glyph.entry_point[1] + glyph.exit_point[1])


def glyph_horizontality(glyph: GlyphRecord) -> float:
    dx = float(glyph.exit_point[0] - glyph.entry_point[0])
    dy = abs(float(glyph.exit_point[1] - glyph.entry_point[1]))
    if dx < 8.0:
        return 0.0
    return float(max(0.0, 1.0 - dy / dx))


def junction_overlap(prev: GlyphRecord, glyph: GlyphRecord) -> int:
    return int(round(JUNCTION_OVERLAP_FACTOR * (prev.average_width + glyph.average_width)))


def set_layout_seed(seed: int | None) -> None:
    global _rng
    _rng = random.Random(seed)


def decide_junction(
    index: int,
    prev: GlyphRecord,
    prev_x: int,
    prev_y: int,
    curr: GlyphRecord,
    x: int,
    y: int,
) -> tuple[str, int]:
    """Random connect / over / under; z-order is assigned separately."""
    _ = (index, prev_x, prev_y)
    pull = junction_overlap(prev, curr)
    mode = _rng.choice(_JUNCTION_MODES)

    if mode == "connect":
        shift = _rng.uniform(0.22, 0.48)
        return "connect", x + int(pull * shift)
    if mode == "under":
        shift = _rng.uniform(0.0, 0.14)
        return "under", x - int(pull * shift)
    shift = _rng.uniform(0.10, 0.24)
    return "over", x - int(pull * shift)


def assign_draw_layers(placed: list[PlacedGlyph]) -> None:
    """Shuffled draw order so later letters do not always cover earlier ones."""
    n = len(placed)
    if n == 0:
        return
    if n == 1:
        placed[0].z_order = 0
        return

    layers = list(range(n))
    _rng.shuffle(layers)

    for i in range(1, n):
        mode = placed[i].blend_mode
        prev_layer = layers[i - 1]
        if mode == "under":
            if layers[i] >= prev_layer:
                layers[i] = prev_layer - 1 - _rng.randint(0, 2)
        elif mode == "over":
            if layers[i] <= prev_layer:
                layers[i] = prev_layer + 1 + _rng.randint(0, 2)
        else:
            layers[i] = prev_layer + _rng.choice([-1, 0, 1])

    min_layer = min(layers)
    layers = [layer - min_layer for layer in layers]

    order = sorted(range(n), key=lambda idx: layers[idx])
    rank = [0] * n
    for draw_rank, glyph_idx in enumerate(order):
        rank[glyph_idx] = draw_rank

    for idx, item in enumerate(placed):
        item.z_order = rank[idx]


def compute_positions(glyphs: list[GlyphRecord]) -> list[tuple[int, int]]:
    if not glyphs:
        return []
    positions: list[tuple[int, int]] = [(0, 0)]
    for index in range(1, len(glyphs)):
        prev = glyphs[index - 1]
        glyph = glyphs[index]
        px, py = positions[-1]

        x = int(round(px + prev.exit_point[0] - glyph.entry_point[0]))
        y = int(round(py + prev.exit_point[1] - glyph.entry_point[1]))

        target_flow = river_flow_y(prev, py)
        current_flow = river_flow_y(glyph, y)
        y += int(round(target_flow - current_flow))

        x -= junction_overlap(prev, glyph)
        positions.append((x, y))
    return positions


def linearity_score(glyphs: list[GlyphRecord]) -> float:
    if len(glyphs) < 2:
        return glyph_horizontality(glyphs[0]) if glyphs else 0.0

    positions = compute_positions(glyphs)
    flow_ys = [river_flow_y(g, y) for g, (_, y) in zip(glyphs, positions)]
    flow_std = float(np.std(flow_ys)) if len(flow_ys) > 1 else 0.0

    score = sum(glyph_horizontality(g) for g in glyphs)
    score -= flow_std * 0.08
    score -= max(0.0, flow_std - 12.0) * 0.15

    for i in range(len(glyphs) - 1):
        left, right = glyphs[i], glyphs[i + 1]
        y_jump = abs(left.exit_point[1] - right.entry_point[1])
        score -= y_jump * 0.012

    return score


def canvas_bounds(placed: list[PlacedGlyph], margin: int = 32) -> tuple[int, int, int, int]:
    if not placed:
        return 0, 0, 800, 400

    min_x = min(p.x for p in placed) - margin
    min_y = min(p.y for p in placed) - margin
    max_x = max(p.x + p.glyph.width for p in placed) + margin
    max_y = max(p.y + p.glyph.height for p in placed) + margin

    for p in placed:
        if p.bridge_before is not None and p.bridge_mask is not None:
            bx, by = p.bridge_offset
            bh, bw = p.bridge_before.shape[:2]
            min_x = min(min_x, bx)
            min_y = min(min_y, by)
            max_x = max(max_x, bx + bw)
            max_y = max(max_y, by + bh)

    width = max(256, max_x - min_x)
    height = max(128, max_y - min_y)
    return min_x, min_y, width, height


def shift_placed(placed: list[PlacedGlyph], offset_x: int, offset_y: int) -> list[PlacedGlyph]:
    shifted: list[PlacedGlyph] = []
    for p in placed:
        bx, by = p.bridge_offset
        shifted.append(
            PlacedGlyph(
                glyph=p.glyph,
                x=p.x - offset_x,
                y=p.y - offset_y,
                index=p.index,
                blend_mode=p.blend_mode,
                z_order=p.z_order,
                bridge_before=p.bridge_before,
                bridge_mask=p.bridge_mask,
                bridge_offset=(bx - offset_x, by - offset_y),
            )
        )
    return shifted

from __future__ import annotations

import numpy as np

from river_engine.blending import build_river_mask
from river_engine.bridge import BridgeBuilder
from river_engine.geometry import angle_diff
from river_engine.layout import assign_draw_layers, compute_positions, decide_junction
from river_engine.types import GlyphRecord, PlacedGlyph


class RiverStitcher:
    def __init__(self, bridge_builder: BridgeBuilder | None = None):
        self.bridge_builder = bridge_builder or BridgeBuilder()

    def connection_score(
        self,
        left: GlyphRecord,
        right: GlyphRecord,
    ) -> float:
        angle_penalty = angle_diff(left.exit_angle, right.entry_angle) / 45.0
        width_ratio = left.average_width / max(right.average_width, 1.0)
        width_penalty = abs(np.log(width_ratio))
        y_misalign = abs(left.exit_point[1] - right.entry_point[1])
        y_penalty = y_misalign / 35.0
        gap = float(np.linalg.norm(right.entry_point - left.exit_point))
        gap_penalty = min(1.0, gap / 80.0)
        strength = 0.5 * (left.connection_strength + right.connection_strength)
        score = (
            1.4 * strength
            - 0.7 * angle_penalty
            - 0.3 * width_penalty
            - 0.65 * y_penalty
            - 0.35 * gap_penalty
        )
        return float(score)

    def place_sequence(
        self,
        glyphs: list[GlyphRecord],
    ) -> list[PlacedGlyph]:
        if not glyphs:
            return []

        positions = compute_positions(glyphs)
        placed: list[PlacedGlyph] = []

        for index, (glyph, (x, y)) in enumerate(zip(glyphs, positions)):
            if index == 0:
                blend_mode = "over"
                z_order = 0
            else:
                prev_placed = placed[-1]
                prev = prev_placed.glyph
                blend_mode, x = decide_junction(
                    index,
                    prev,
                    prev_placed.x,
                    prev_placed.y,
                    glyph,
                    x,
                    y,
                )
                z_order = 0

            bridge_patch = None
            bridge_mask = None
            bridge_offset = (0, 0)

            if index > 0:
                prev = placed[-1].glyph
                prev_exit = prev.exit_point + np.array([placed[-1].x, placed[-1].y])
                entry_world = glyph.entry_point + np.array([x, y])
                ang = angle_diff(prev.exit_angle, glyph.entry_angle)
                gap = float(np.linalg.norm(entry_world - prev_exit))
                if gap > 6.0 and self.bridge_builder.needs_bridge(
                    prev_exit, entry_world, ang
                ):
                    bridge_patch, bridge_mask, bridge_offset = self.bridge_builder.build(
                        prev_exit,
                        entry_world,
                        prev.exit_angle,
                        glyph.entry_angle,
                        0.5 * (prev.average_width + glyph.average_width),
                        seed=index * 17,
                    )

            placed.append(
                PlacedGlyph(
                    glyph=glyph,
                    x=x,
                    y=y,
                    index=index,
                    blend_mode=blend_mode,
                    z_order=z_order,
                    bridge_before=bridge_patch,
                    bridge_mask=bridge_mask,
                    bridge_offset=bridge_offset,
                )
            )
        assign_draw_layers(placed)
        return placed

    def river_mask_for_glyph(self, placed: PlacedGlyph) -> np.ndarray:
        g = placed.glyph
        pts = g.river_points + np.array([placed.x, placed.y])
        h = max(g.height, int(pts[:, 1].max()) + 8)
        w = max(g.width, int(pts[:, 0].max()) + 8)
        return build_river_mask(pts, (h, w), int(round(g.average_width)))

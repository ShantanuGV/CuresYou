from __future__ import annotations

import cv2
import numpy as np

from river_engine.blending import (
    alpha_blend,
    alpha_under,
    build_river_mask,
)

from river_engine.config import DEFAULT_OUTPUT_SCALE
from river_engine.layout import canvas_bounds, shift_placed
from river_engine.types import CompositionResult, PlacedGlyph


class CompositionRenderer:

    def render(
        self,
        placed: list[PlacedGlyph],
        word: str,
        score: float,
        output_scale: float = DEFAULT_OUTPUT_SCALE,
    ) -> CompositionResult:

        min_x, min_y, width, height = canvas_bounds(placed)

        shifted = shift_placed(
            placed,
            min_x,
            min_y,
        )

        canvas = np.zeros(
            (height, width, 3),
            dtype=np.uint8,
        )

        # draw bridges first
        for item in shifted:

            if (
                item.bridge_before is not None
                and item.bridge_mask is not None
            ):

                bx, by = item.bridge_offset

                bridge_mask = (
                    item.bridge_mask > 0
                ).astype(np.float32)

                canvas = alpha_blend(
                    canvas,
                    item.bridge_before,
                    bridge_mask,
                    (bx, by),
                )

        # render by z-order
        draw_order = sorted(
            shifted,
            key=lambda p: (p.z_order, p.index),
        )

        for item in draw_order:
            canvas = self._paste_glyph(
                canvas,
                item,
            )

        # resize output if needed
        if output_scale != 1.0:

            new_w = max(
                1,
                int(canvas.shape[1] * output_scale),
            )

            new_h = max(
                1,
                int(canvas.shape[0] * output_scale),
            )

            canvas = cv2.resize(
                canvas,
                (new_w, new_h),
                interpolation=cv2.INTER_AREA,
            )

        return CompositionResult(
            canvas=canvas,
            placed=shifted,
            score=score,
            word=word,
        )

    def _river_mask(
        self,
        item: PlacedGlyph,
        ph: int,
        pw: int,
    ) -> np.ndarray:

        """
        Used ONLY for soft blending.
        NEVER for tile visibility/cropping.
        """

        g = item.glyph

        h, w = g.image.shape[:2]

        river_mask = build_river_mask(
            g.river_points,
            (h, w),
            int(round(g.average_width)),
        )[:ph, :pw]

        river_mask = river_mask.astype(np.float32)

        if river_mask.max() > 1.0:
            river_mask /= 255.0

        return river_mask

    def _paste_glyph(
        self,
        canvas: np.ndarray,
        item: PlacedGlyph,
    ) -> np.ndarray:

        g = item.glyph

        x, y = item.x, item.y

        patch = g.image

        h, w = patch.shape[:2]

        # clipping to canvas
        y1 = min(canvas.shape[0], y + h)
        x1 = min(canvas.shape[1], x + w)

        ph = y1 - y
        pw = x1 - x

        if ph <= 0 or pw <= 0:
            return canvas

        region = patch[:ph, :pw]

        # IMPORTANT:
        # FULL RECTANGULAR TILE MASK
        # NO LETTER SHAPE MASKING
        # NO RIVER SHAPE CROPPING
        full_mask = np.ones(
            (ph, pw),
            dtype=np.float32,
        )

        # optional river softness
        river_mask = self._river_mask(
            item,
            ph,
            pw,
        )

        mode = item.blend_mode

        # -----------------------------------
        # UNDERLAP
        # -----------------------------------
        if mode == "under":

            # full rectangular tile under
            canvas = alpha_under(
                canvas,
                region,
                full_mask,
                (x, y),
            )

            # optional soft river reinforcement
            canvas = alpha_blend(
                canvas,
                region,
                river_mask * 0.15,
                (x, y),
            )

        # -----------------------------------
        # OVER / CONNECT
        # -----------------------------------
        else:

            canvas = alpha_blend(
                canvas,
                region,
                full_mask,
                (x, y),
            )

        return canvas

    @staticmethod
    def save(
        result: CompositionResult,
        path: str,
    ) -> None:

        path_lower = path.lower()

        if path_lower.endswith(".png"):

            cv2.imwrite(
                path,
                result.canvas,
                [cv2.IMWRITE_PNG_COMPRESSION, 3],
            )

        else:

            cv2.imwrite(
                path,
                result.canvas,
                [cv2.IMWRITE_JPEG_QUALITY, 95],
            )
from __future__ import annotations

from pathlib import Path

from river_engine.config import DEFAULT_OUTPUT_SCALE, OUTPUT_DIR
from river_engine.debug import draw_debug_overlay
from river_engine.metadata_loader import index_all_metadata
from river_engine.optimizer import CandidateOptimizer
from river_engine.renderer import CompositionRenderer
from river_engine.stitcher import RiverStitcher


class RiverWordPipeline:
    def __init__(
        self,
        output_scale: float = DEFAULT_OUTPUT_SCALE,
        debug: bool = False,
    ):
        self.catalog = index_all_metadata()
        self.optimizer = CandidateOptimizer(RiverStitcher())
        self.stitcher = RiverStitcher()
        self.renderer = CompositionRenderer()
        self.output_scale = output_scale
        self.debug = debug

    def generate(self, word: str) -> Path:
        cleaned = "".join(ch for ch in word.strip() if ch.isalpha())
        if not cleaned:
            raise ValueError("Word must contain at least one letter")

        glyphs = self.optimizer.search(cleaned, self.catalog)
        placed = self.stitcher.place_sequence(glyphs)
        score = self.optimizer._score_sequence(glyphs)
        result = self.renderer.render(
            placed,
            cleaned,
            score=score,
            output_scale=self.output_scale,
        )

        if self.debug:
            result.canvas = draw_debug_overlay(result.canvas, result.placed)

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out_name = cleaned.lower()
        out_path = OUTPUT_DIR / f"{out_name}.png"
        flat_path = Path.cwd() / "output.png"

        CompositionRenderer.save(result, str(out_path))
        CompositionRenderer.save(result, str(flat_path))
        return out_path

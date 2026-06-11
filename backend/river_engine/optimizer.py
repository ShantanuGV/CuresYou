from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Iterable

from river_engine.config import (
    CANDIDATES_PER_LETTER,
    MAX_OPTIMIZER_COMBINATIONS,
    OPTIMIZER_BEAM_WIDTH,
)
from river_engine.layout import glyph_horizontality, linearity_score
from river_engine.normalizer import normalize_glyph
from river_engine.stitcher import RiverStitcher
from river_engine.types import GlyphRecord


@dataclass
class _BeamState:
    score: float
    glyphs: list[GlyphRecord]


class CandidateOptimizer:
    def __init__(
        self,
        stitcher: RiverStitcher | None = None,
        candidates_per_letter: int = CANDIDATES_PER_LETTER,
        beam_width: int = OPTIMIZER_BEAM_WIDTH,
    ):
        self.stitcher = stitcher or RiverStitcher()
        self.candidates_per_letter = candidates_per_letter
        self.beam_width = beam_width

    def _letter_quality(self, glyph: GlyphRecord) -> float:
        lb = glyph.letter_bbox
        letter_w = max(1, lb[2] - lb[0])
        letter_h = max(1, lb[3] - lb[1])
        letter_area = letter_w * letter_h
        image_area = max(1, glyph.width * glyph.height)
        compactness = letter_area / image_area

        meta = glyph.metadata
        readable = 1.0 if meta.get("contains_readable_letter", True) else 0.0
        point_density = min(1.2, len(glyph.letter_points) / 350.0)
        path_len = float(meta.get("letter_path_length", len(glyph.letter_points)))
        path_score = min(1.0, path_len / 500.0)

        river_area = max(
            1,
            (glyph.river_bbox[2] - glyph.river_bbox[0])
            * (glyph.river_bbox[3] - glyph.river_bbox[1]),
        )
        river_tightness = letter_area / river_area
        tilt_penalty = abs(glyph.rotation_deg) * 0.15
        horizontal = glyph_horizontality(glyph) * 1.8

        return float(
            1.4 * readable
            + 1.1 * point_density
            + 0.9 * path_score
            + 1.3 * compactness
            + 0.6 * river_tightness
            + horizontal
            + glyph.connection_strength
            - 0.0004 * image_area
            - tilt_penalty
        )

    def _pair_score(self, left: GlyphRecord, right: GlyphRecord) -> float:
        return self.stitcher.connection_score(left, right) * 3.2

    def search(
        self,
        word: str,
        catalog: dict[str, list[GlyphRecord]],
    ) -> list[GlyphRecord]:
        letters = [ch for ch in word.lower() if ch.isalpha()]
        if not letters:
            return []

        pools: list[list[GlyphRecord]] = []
        for letter in letters:
            pool = catalog.get(letter, [])
            if not pool:
                raise ValueError(f"No glyph candidates for letter '{letter}'")
            pools.append(pool)

        normalized_pools = [[normalize_glyph(g) for g in pool] for pool in pools]
        total_combos = 1
        for pool in normalized_pools:
            total_combos *= len(pool)

        if total_combos <= MAX_OPTIMIZER_COMBINATIONS:
            return self._exhaustive(normalized_pools)
        return self._beam_search(normalized_pools)

    def _exhaustive(self, pools: list[list[GlyphRecord]]) -> list[GlyphRecord]:
        best: list[GlyphRecord] = []
        best_score = float("-inf")
        for combo in itertools.product(*pools):
            seq = list(combo)
            score = self._score_sequence(seq)
            if score > best_score:
                best_score = score
                best = seq
        return best

    def _beam_search(self, pools: list[list[GlyphRecord]]) -> list[GlyphRecord]:
        first_pool = self._top_for_position(pools[0], None)
        states = [_BeamState(self._letter_quality(g), [g]) for g in first_pool]
        states.sort(key=lambda s: s.score, reverse=True)
        states = states[: self.beam_width]

        for pool in pools[1:]:
            candidates = self._top_for_position(pool, None)
            next_states: list[_BeamState] = []
            for state in states:
                prev = state.glyphs[-1]
                for glyph in candidates:
                    partial = state.glyphs + [glyph]
                    step = (
                        self._letter_quality(glyph)
                        + self._pair_score(prev, glyph)
                        + linearity_score(partial) * 0.35
                    )
                    next_states.append(_BeamState(state.score + step, partial))
            next_states.sort(key=lambda s: s.score, reverse=True)
            states = next_states[: self.beam_width]

        if not states:
            return self._greedy(pools)
        return states[0].glyphs

    def _top_for_position(
        self,
        pool: list[GlyphRecord],
        previous: GlyphRecord | None,
    ) -> list[GlyphRecord]:
        scored: list[tuple[float, GlyphRecord]] = []
        for glyph in pool:
            score = self._letter_quality(glyph)
            if previous is not None:
                score += self._pair_score(previous, glyph)
            scored.append((score, glyph))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [g for _, g in scored[: self.candidates_per_letter]]

    def _greedy(self, pools: list[list[GlyphRecord]]) -> list[GlyphRecord]:
        chosen: list[GlyphRecord] = []
        previous: GlyphRecord | None = None
        for pool in pools:
            ranked = self._top_for_position(pool, previous)
            pick = ranked[0]
            chosen.append(pick)
            previous = pick
        return chosen

    def _score_sequence(self, glyphs: list[GlyphRecord]) -> float:
        if not glyphs:
            return float("-inf")
        total = sum(self._letter_quality(g) for g in glyphs)
        total += linearity_score(glyphs) * 2.5
        for i in range(len(glyphs) - 1):
            total += self._pair_score(glyphs[i], glyphs[i + 1])
        widths = [g.average_width for g in glyphs]
        total -= _np_std(widths) * 0.12
        return total


def _np_std(values: Iterable[float]) -> float:
    arr = list(values)
    if len(arr) < 2:
        return 0.0
    mean = sum(arr) / len(arr)
    return (sum((v - mean) ** 2 for v in arr) / len(arr)) ** 0.5

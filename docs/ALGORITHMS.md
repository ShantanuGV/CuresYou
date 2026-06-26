# Algorithms

---

# Introduction

CurseYou is not a traditional font renderer.

Instead of drawing predefined glyphs, the engine searches a collection of river glyph candidates, evaluates their compatibility, determines an optimal sequence, computes their spatial layout, and finally renders them into a continuous river composition.

The backend combines several algorithmic techniques from computational geometry, heuristic optimization, and digital image processing.

---

# Algorithm Overview

The complete generation pipeline consists of the following stages:

```text
              Input Word
                   │
                   ▼
        Character Normalization
                   │
                   ▼
          Metadata Retrieval
                   │
                   ▼
         Candidate Collection
                   │
                   ▼
        Beam Search Optimization
                   │
                   ▼
         Sequence Evaluation
                   │
                   ▼
          Layout Computation
                   │
                   ▼
         Junction Assignment
                   │
                   ▼
          Bridge Generation
                   │
                   ▼
           Image Blending
                   │
                   ▼
          Final Composition
```

Each stage is independent and performs a specific responsibility within the rendering pipeline.

---

# 1. Candidate Retrieval

Each character may have multiple river glyphs stored in the dataset.

Example:

```text
Letter A

↓

A₁

A₂

A₃

A₄

A₅
```

Instead of selecting a glyph immediately, all available candidates are collected for later evaluation.

This allows the optimizer to search for combinations that produce better continuity between neighboring characters.

---

# 2. Beam Search Optimization

## Purpose

The optimizer searches for the most compatible sequence of glyphs while avoiding the exponential cost of evaluating every possible combination.

Suppose every character has:

```
12 candidates
```

For an eight-letter word:

```
12⁸

=

429,981,696
```

possible combinations would exist.

Evaluating every possibility would be impractical.

Beam Search reduces this complexity by retaining only the highest-scoring partial solutions after each expansion.

---

## Beam Search Workflow

```text
Input Word

↓

Expand Candidates

↓

Evaluate Scores

↓

Sort Candidates

↓

Keep Top-K States

↓

Expand Again

↓

Repeat Until Complete

↓

Best Sequence
```

Only the best states survive each iteration.

---

## Advantages

* Significantly reduces computation.
* Produces high-quality sequences.
* Maintains deterministic behavior.
* Scales efficiently for longer words.

---

# 3. Sequence Scoring

Every candidate sequence is evaluated using several heuristic scoring functions.

The optimizer favors sequences that preserve visual continuity.

The implementation combines multiple metrics rather than relying on a single score.

Examples include:

* connection quality
* horizontality
* linearity
* width consistency
* junction compatibility

The combined score determines which Beam Search states remain active.

---

# 4. Connection Scoring

Neighboring glyphs should connect naturally.

The connection score evaluates:

* relative orientation
* connection geometry
* river width compatibility

Poor connections receive penalties while smooth transitions receive higher scores.

This improves overall visual coherence.

---

# 5. Horizontality Evaluation

Words generally read from left to right.

The optimizer therefore prefers glyph sequences that progress horizontally.

Large vertical deviations reduce readability and receive lower scores.

This heuristic helps maintain a natural reading flow.

---

# 6. Linearity Evaluation

The backend also measures how smoothly the river progresses throughout the word.

Abrupt changes in direction reduce the linearity score.

Smooth transitions receive higher scores.

Together with horizontality, this prevents unstable layouts.

---

# 7. Candidate Pruning

Beam Search naturally produces many partial solutions.

The optimizer periodically removes low-scoring candidates.

This process is known as pruning.

Pruning reduces:

* memory usage
* computation time
* unnecessary evaluations

while preserving promising solutions.

---

# 8. Layout Computation

After the optimal sequence has been selected, the layout engine computes the position of every glyph.

Rather than using fixed coordinates, each glyph is positioned relative to its predecessor.

```text
Glyph 1

↓

Glyph 2

↓

Glyph 3

↓

Glyph 4
```

The layout engine computes:

* placement
* overlap
* offsets
* canvas bounds

before rendering begins.

---

# 9. Junction Assignment

Neighboring glyphs may connect in different ways.

The stitching engine determines which junction mode should be used.

Possible modes include:

```text
Connect

Over

Under
```

The selected mode determines how two river segments interact during rendering.

---

# 10. Bridge Generation

Not every pair of glyphs naturally connects.

Before generating a bridge, the engine evaluates whether a bridge is actually required.

The decision considers:

* distance between glyph endpoints
* angular difference

Only when these measurements exceed predefined thresholds is a bridge created.

This avoids unnecessary bridge generation.

---

## Bridge Workflow

```text
Glyph A

↓

Gap Analysis

↓

Bridge Needed?

↓

Yes

↓

Generate Bridge

↓

Continue Rendering
```

Otherwise, the existing glyphs are connected directly.

---

# 11. Feather Mask Generation

When multiple river images overlap, visible seams may appear.

The blending module constructs feather masks that gradually transition between neighboring images.

Instead of abrupt boundaries,

the overlap region becomes progressively transparent.

This creates smoother transitions.

---

# 12. Alpha Blending

After masks are generated, the renderer combines river segments through alpha compositing.

The blending stage merges overlapping imagery while preserving the underlying texture.

Responsibilities include:

* transparency handling
* overlap blending
* seam reduction
* compositing

---

# 13. Rendering Pipeline

The renderer converts positioned glyphs into the final image.

Rendering consists of:

```text
Canvas Allocation

↓

Position Adjustment

↓

Mask Generation

↓

Image Blending

↓

Bridge Rendering

↓

PNG Export
```

The renderer performs no optimization.

Its responsibility is purely visual composition.

---

# 14. Shared Geometry Algorithms

Several mathematical helper algorithms are reused throughout the project.

Examples include:

* path length computation
* angle computation
* angle difference
* point interpolation
* geometric transformations

These utilities are centralized to avoid duplicated implementations.

---

# Computational Complexity

The exact running time depends on:

* word length
* number of glyph candidates
* Beam width
* rendering resolution

Approximate behavior is summarized below.

| Stage               | Relative Cost |
| ------------------- | ------------- |
| Metadata Loading    | Low           |
| Candidate Retrieval | Low           |
| Beam Search         | High          |
| Layout Computation  | Medium        |
| Junction Assignment | Low           |
| Bridge Generation   | Medium        |
| Image Blending      | Medium        |
| Rendering           | High          |

The optimizer is the most computationally intensive stage, while rendering dominates execution time for large output images.

---

# Design Decisions

The backend intentionally separates optimization from rendering.

This provides several advantages:

* rendering improvements do not affect search algorithms
* optimization strategies can evolve independently
* modules remain easier to test
* responsibilities stay clearly defined

The result is a modular architecture where each component performs one well-defined task.

---

# Summary

CurseYou combines techniques from multiple areas of computer science to procedurally generate continuous river typography.

The backend integrates:

* Beam Search optimization
* heuristic candidate scoring
* geometric layout computation
* junction analysis
* conditional bridge generation
* feather mask generation
* alpha compositing
* raster image rendering

Rather than relying on predefined fonts, the engine dynamically constructs every word by selecting, arranging, and blending compatible river glyphs into a single continuous composition.

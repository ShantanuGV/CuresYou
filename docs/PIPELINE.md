# Pipeline

---

# Introduction

The CurseYou backend follows a deterministic multi-stage processing pipeline that transforms an input text string into a procedurally generated river composition.

Rather than rendering predefined font glyphs, the engine constructs every word dynamically by selecting compatible river glyphs, computing their geometric relationships, and blending them into a single continuous image.

Each processing stage has a single responsibility and passes its output to the next stage.

---

# Complete Pipeline

```text
                 User Input
                      │
                      ▼
            Character Processing
                      │
                      ▼
             Metadata Loading
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
        Junction Determination
                      │
                      ▼
          Bridge Generation
                      │
                      ▼
          Canvas Allocation
                      │
                      ▼
         Image Compositing
                      │
                      ▼
            PNG Generation
```

Each stage is independent and contributes one specific task to the rendering process.

---

# Stage 1 — User Input

The pipeline begins with a text string supplied by the user.

Example

```text
CURSEYOU
```

The backend receives the input and prepares it for processing.

At this stage, no rendering has occurred.

---

# Stage 2 — Character Processing

The input string is decomposed into individual characters.

Example

```text
CURSEYOU

↓

C
U
R
S
E
Y
O
U
```

Each character becomes an independent processing unit.

The remaining stages operate on these characters rather than the original string.

---

# Stage 3 — Metadata Loading

The metadata loader retrieves every available river glyph corresponding to each character.

Instead of loading only images, this stage constructs structured glyph objects containing:

* geometric information
* connection metadata
* image references
* width information
* orientation data

These objects become the working representation used throughout the pipeline.

---

# Stage 4 — Candidate Collection

Most characters have multiple possible river representations.

Example

```text
Letter A

↓

A₁

A₂

A₃

A₄
```

Rather than selecting one immediately, every valid candidate is collected.

This allows the optimizer to evaluate many possible combinations before making a decision.

---

# Stage 5 — Beam Search Optimization

This is the core decision-making stage.

Instead of evaluating every possible glyph combination, the optimizer performs Beam Search.

The search expands candidate sequences incrementally while retaining only the highest-scoring partial solutions.

The evaluation considers factors implemented by the backend, including:

* connection quality
* horizontality
* linearity
* width compatibility
* junction consistency

At the end of this stage, the engine produces a single optimized sequence of river glyphs.

---

# Stage 6 — Sequence Evaluation

The selected sequence undergoes additional compatibility checks before layout begins.

Neighbouring glyphs are analysed to ensure that transitions remain visually consistent.

This stage prepares the data required by the stitching and layout components.

---

# Stage 7 — Layout Computation

The layout engine computes where every glyph should appear on the final canvas.

Instead of assigning fixed coordinates, placement is determined relative to previously positioned glyphs.

The layout process computes:

* glyph offsets
* overlap positions
* canvas boundaries
* horizontal progression

No pixels are rendered during this stage.

Only spatial relationships are established.

---

# Stage 8 — Junction Determination

For every neighbouring glyph pair, the stitcher determines how the transition should occur.

Possible junction modes include:

```text
Connect

Over

Under
```

The selected mode determines how the renderer will composite the river segments.

---

# Stage 9 — Bridge Generation

Not every neighbouring glyph connects naturally.

The bridge builder evaluates whether a connecting bridge is required.

The decision is based on geometric analysis, including:

* endpoint separation
* orientation difference

If a bridge is required, smooth transition geometry is generated.

Otherwise, the existing river segments are connected directly.

---

# Stage 10 — Canvas Allocation

After every glyph position has been computed, the renderer determines the minimum canvas size required to contain the complete composition.

The bounding box is calculated from the positioned glyphs.

Only then is the output image allocated.

This minimizes unnecessary memory usage.

---

# Stage 11 — Image Compositing

The renderer begins assembling the final image.

During this stage the engine:

* places river glyphs
* generates blending masks
* performs alpha compositing
* renders bridges
* resolves overlapping regions

The renderer operates exclusively on positioned glyphs produced by earlier stages.

No optimization decisions occur here.

---

# Stage 12 — PNG Generation

The completed composition is exported as the final output image.

The generated PNG represents the fully stitched river typography.

Example

```text
Input

CURSEYOU

↓

Processing Pipeline

↓

Continuous River Typography
```

---

# Data Flow

Throughout execution, the backend transforms data through several representations.

```text
Input String

↓

Characters

↓

Glyph Metadata

↓

Candidate Glyphs

↓

Optimized Sequence

↓

Positioned Glyphs

↓

Rendered Layers

↓

Final PNG
```

Each stage consumes the previous representation and produces a richer one.

---

# Module Interaction

The pipeline is implemented through cooperating backend modules.

```text
main.py / server.py
        │
        ▼
pipeline.py
        │
        ▼
metadata_loader.py
        │
        ▼
optimizer.py
        │
        ▼
stitcher.py
     ┌──┴──┐
     ▼     ▼
layout.py bridge.py
     └──┬──┘
        ▼
renderer.py
        │
        ▼
blending.py
```

The geometry utilities provide shared mathematical operations used across multiple stages.

---

# Error Handling

The pipeline is designed so that each stage operates independently.

If an earlier stage cannot provide valid data, downstream stages are prevented from executing on incomplete information.

This modular structure simplifies debugging and improves maintainability.

---

# Design Characteristics

The processing pipeline follows several important design principles.

### Deterministic

Given identical input, metadata, and configuration, the pipeline produces consistent output.

---

### Modular

Every stage performs one clearly defined task.

This separation reduces coupling and simplifies future development.

---

### Extensible

New optimization strategies, rendering techniques, or bridge generation methods can be introduced without redesigning the complete pipeline.

---

### Sequential

Each stage depends only on the output of the previous stage.

This creates a predictable and maintainable execution flow.

---

# Pipeline Summary

The CurseYou backend transforms a text string into continuous river typography through a structured sequence of processing stages.

The overall execution flow is:

```text
Input

↓

Metadata Loading

↓

Candidate Collection

↓

Beam Search Optimization

↓

Layout Computation

↓

Junction Determination

↓

Bridge Generation

↓

Image Compositing

↓

PNG Export
```

By separating optimization, geometry, stitching, and rendering into independent stages, the backend remains modular, maintainable, and extensible while producing visually continuous river compositions.

# Architecture

---

# CurseYou System Architecture

CurseYou is designed as a modular procedural graphics engine.

Instead of placing all logic inside one script, the backend separates the generation process into independent components responsible for metadata loading, candidate optimization, geometric layout, stitching, image blending, and final rendering.

Each module has a single responsibility and communicates through well-defined data structures.

This architecture makes the engine easier to understand, maintain, and extend.

---

# High-Level Architecture

```text
                        User Input
                             │
                             ▼
                      Metadata Loader
                             │
                             ▼
                  Candidate Optimizer
                             │
                             ▼
                     River Stitcher
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
            Layout Engine        Bridge Builder
                  │                     │
                  └──────────┬──────────┘
                             ▼
                    Composition Renderer
                             │
                             ▼
                        PNG Generation
```

---

# Backend Directory Structure

```text
backend/
│
├── main.py
├── server.py
│
└── river_engine/
    ├── metadata_loader.py
    ├── optimizer.py
    ├── stitcher.py
    ├── layout.py
    ├── bridge.py
    ├── renderer.py
    ├── blending.py
    ├── geometry.py
```

Every module performs one specific task.

---

# Design Philosophy

The backend follows three principles.

## Modular Design

Each module is responsible for one stage of the pipeline.

Examples:

- metadata loading
- optimization
- layout
- stitching
- rendering

This minimizes coupling between components.

---

## Data-Driven Processing

The engine operates on metadata rather than directly manipulating raw images.

River images are treated as graphical assets while geometric information drives decision making.

---

## Procedural Composition

Every output image is synthesized during execution.

No complete words are stored.

Only individual river glyphs are available, and every word is assembled dynamically.

---

# Component Overview

| Module | Responsibility |
|---------|----------------|
| metadata_loader.py | Loads glyph metadata and associated images |
| optimizer.py | Searches for the best glyph sequence |
| stitcher.py | Connects neighbouring glyphs |
| layout.py | Computes glyph placement |
| bridge.py | Generates bridge segments when required |
| renderer.py | Produces the final image |
| blending.py | Image blending and masking |
| geometry.py | Shared geometric utilities |

---

# System Data Flow

```text
Input Word

      │

      ▼

Metadata Loading

      │

      ▼

Candidate Selection

      │

      ▼

Sequence Optimization

      │

      ▼

Glyph Placement

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

---

# Module Details

---

## Metadata Loader

**File**

```text
metadata_loader.py
```

### Purpose

The metadata loader is responsible for reading glyph metadata and locating the corresponding river imagery.

Instead of searching image folders manually during rendering, this module builds structured glyph objects before the optimization stage begins.

### Responsibilities

- locate metadata files
- resolve image paths
- load river images
- convert point arrays into geometric data
- create glyph records

### Output

A collection of glyph records used throughout the pipeline.

---

## Candidate Optimizer

**File**

```text
optimizer.py
```

### Purpose

The optimizer determines which river candidate should represent every character.

Each letter may have multiple possible glyphs.

Rather than selecting the first available candidate, the optimizer evaluates different combinations and searches for the highest-scoring sequence.

### Internal Strategy

The optimizer uses Beam Search.

Instead of exploring every possible combination,

```
candidates^letters
```

it keeps only the highest-scoring partial solutions after every expansion.

This dramatically reduces the search space.

### Responsibilities

- normalize glyphs
- generate candidate combinations
- maintain beam states
- prune low-scoring solutions
- return the best sequence

---

## River Stitcher

**File**

```text
stitcher.py
```

### Purpose

The stitcher connects neighbouring glyphs into a continuous composition.

It evaluates compatibility between consecutive glyphs and computes how they should be joined.

### Responsibilities

- compute connection scores
- evaluate angle compatibility
- compare river widths
- assign junction modes
- invoke bridge generation when necessary

The stitcher acts as the central coordination module between optimization and rendering.

---

## Layout Engine

**File**

```text
layout.py
```

### Purpose

The layout engine determines where every glyph should appear on the canvas.

Rather than placing glyphs at fixed coordinates, positions are computed dynamically.

### Responsibilities

- compute glyph positions
- estimate river flow
- calculate junction overlap
- measure glyph horizontality
- compute canvas bounds
- shift final composition

It also determines drawing order for overlapping glyphs.

---

## Bridge Builder

**File**

```text
bridge.py
```

### Purpose

Some neighbouring glyphs cannot be connected directly.

The bridge builder generates transition geometry between them.

### Important Behaviour

A bridge is **not** always created.

Before generating one, the engine evaluates:

- gap distance
- angle difference

If the gap exceeds the configured threshold or the angular difference becomes sufficiently large, a bridge is generated.

Otherwise, the glyphs are connected directly.

This avoids unnecessary bridge creation.

---

## Renderer

**File**

```text
renderer.py
```

### Purpose

The renderer converts positioned glyphs into the final image.

This module is responsible only for visual composition.

It does not decide which glyphs should be used.

### Responsibilities

- allocate output canvas
- shift glyph positions
- build masks
- perform image compositing
- apply scaling
- produce final output

The renderer represents the final stage of the pipeline.

---

## Blending Module

**File**

```text
blending.py
```

### Purpose

Image blending removes visible seams between neighbouring river segments.

### Responsibilities

- generate feather masks
- alpha blending
- under compositing
- river mask generation

Gaussian blur is used when constructing feather masks to produce smoother transitions between overlapping regions.

---

## Geometry Utilities

**File**

```text
geometry.py
```

### Purpose

Shared mathematical functions used throughout the backend.

### Responsibilities

- point conversion
- path length computation
- angle calculation
- angle difference
- spline interpolation utilities
- geometric helper functions

These utilities are reused by multiple modules and avoid duplicated mathematical code.

---

# Module Dependency Graph

```text
                 metadata_loader
                        │
                        ▼
                   optimizer
                        │
                        ▼
                    stitcher
                  ┌─────┴─────┐
                  ▼           ▼
               layout      bridge
                  │           │
                  └─────┬─────┘
                        ▼
                    renderer
                        │
                        ▼
                    blending

geometry
   ▲
   │
Used throughout the engine
```

---

# Separation of Responsibilities

The backend intentionally separates decision making from rendering.

| Decision Layer | Rendering Layer |
|---------------|-----------------|
| Metadata loading | Image blending |
| Candidate optimization | Alpha compositing |
| Layout computation | Canvas generation |
| Stitching | PNG export |

This separation allows rendering improvements without changing optimization logic.

---

# Execution Lifecycle

```text
1. Receive input word

↓

2. Load metadata

↓

3. Retrieve candidates

↓

4. Optimize glyph sequence

↓

5. Compute layout

↓

6. Stitch neighbouring glyphs

↓

7. Generate bridges when required

↓

8. Blend river imagery

↓

9. Render composition

↓

10. Export final image
```

---

# Extensibility

The modular architecture allows future improvements without redesigning the entire engine.

Possible extensions include:

- additional glyph datasets
- alternative optimization strategies
- improved bridge generation
- enhanced rendering techniques
- additional export formats

Because responsibilities are isolated, these enhancements can be introduced with minimal impact on existing modules.

---

# Summary

CurseYou is structured as a pipeline of independent components that transform a text string into a procedurally generated river composition.

Each module performs one clearly defined task:

- **Metadata Loader** prepares structured glyph data.
- **Candidate Optimizer** selects the best sequence.
- **River Stitcher** connects neighbouring glyphs.
- **Layout Engine** computes placement.
- **Bridge Builder** fills geometric gaps when necessary.
- **Blending Module** creates smooth visual transitions.
- **Renderer** produces the final output image.

This separation of concerns makes the engine easier to understand, test, and extend while keeping the processing pipeline organized and maintainable.

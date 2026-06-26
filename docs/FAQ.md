# Frequently Asked Questions (FAQ)

---

# General Questions

## What is CurseYou?

CurseYou is a procedural river typography engine that generates readable words using real river geometries instead of traditional fonts.

Instead of storing complete words, the engine dynamically assembles individual river glyphs into a continuous river composition.

---

## Is CurseYou an AI or Machine Learning project?

No.

The current implementation does **not** use machine learning or neural networks.

Instead, it relies on:

* metadata-driven glyph retrieval
* Beam Search optimization
* computational geometry
* heuristic scoring
* image compositing
* procedural rendering

---

## How is this different from a font?

Traditional fonts contain predefined vector glyphs.

CurseYou does not.

Every character has multiple river representations stored in the dataset.

During execution, the backend selects compatible glyphs and procedurally assembles them into a new composition.

Every rendered word is generated at runtime.

---

## Are the generated words pre-rendered?

No.

Only individual river glyphs are stored.

Every output word is constructed dynamically during execution.

---

## What programming language is used?

The backend is written in **Python**.

The frontend is built separately and communicates with the backend through HTTP requests.

---

## Which algorithm selects the glyphs?

The backend uses **Beam Search**.

Beam Search explores multiple candidate sequences while keeping only the highest-scoring partial solutions.

This allows the engine to generate high-quality results without evaluating every possible combination.

---

## Does the engine use vector graphics?

No.

The current implementation operates primarily on raster images and metadata.

Geometric information is used for positioning and stitching, while rendering is performed through image compositing.

---

# Rendering Questions

## Why doesn't the engine simply place images next to each other?

Adjacent placement would create:

* visible seams
* discontinuous rivers
* inconsistent widths
* unnatural transitions

Instead, the backend evaluates compatibility, computes layout, generates bridges when required, and blends neighboring glyphs into a continuous composition.

---

## Are bridges always generated?

No.

The bridge generation module first determines whether a bridge is necessary.

If neighboring glyphs already connect naturally, no bridge is created.

---

## How are visible seams removed?

The renderer uses:

* feather masks
* alpha blending
* overlap handling

These techniques produce smoother transitions between neighboring river glyphs.

---

## Can every word be generated?

The engine can generate words using characters available in the dataset.

The quality of the result depends on:

* available glyph candidates
* optimization
* compatibility between neighboring letters

---

# Technical Questions

## Why use Beam Search instead of exhaustive search?

An exhaustive search becomes computationally expensive as word length increases.

Beam Search dramatically reduces the search space while still producing high-quality solutions.

---

## Why is the project modular?

Separating the backend into independent modules provides several benefits:

* easier maintenance
* improved readability
* independent testing
* future extensibility

Each module has one well-defined responsibility.

---

## Which modules perform rendering?

Rendering is primarily handled by:

* `renderer.py`
* `bridge.py`
* `blending.py`

Optimization and layout occur before rendering begins.

---

## Does the backend modify the original dataset?

No.

The original river glyphs remain unchanged.

The backend generates new compositions by positioning and blending copies of those glyphs.

---

# Development Questions

## Can I add new river glyphs?

Yes.

The engine is designed to work with metadata-driven glyph datasets.

Adding properly formatted glyphs expands the available search space and may improve rendering quality.

---

## Can I replace the optimization algorithm?

Yes.

The modular architecture allows the optimizer to be replaced or extended without redesigning the rendering pipeline.

---

## Can I use another rendering backend?

Potentially.

Since optimization, layout, and rendering are separated, a different renderer could be implemented while preserving the existing optimization pipeline.

---

# Future Development

## What improvements are planned?

Potential future enhancements include:

* additional glyph datasets
* improved optimization strategies
* GPU-accelerated rendering
* SVG export
* batch processing
* interactive editor
* higher-quality bridge generation

See **ROADMAP.md** for more information.

---

# Repository Questions

## Where should I start reading the code?

Recommended order:

```text
README.md
        ↓
PROJECT_OVERVIEW.md
        ↓
ARCHITECTURE.md
        ↓
PIPELINE.md
        ↓
ALGORITHMS.md
        ↓
MATHEMATICS.md
        ↓
backend/
```

---

## How can I contribute?

Please read **CONTRIBUTING.md** before submitting issues or pull requests.

---

## Which license is used?

CurseYou is released under the **MIT License**.

See **LICENSE** for complete details.

---

# Summary

CurseYou is a procedural graphics engine that combines computational geometry, heuristic optimization, and image compositing to generate continuous river typography.

Rather than rendering predefined fonts, the backend dynamically constructs each word from compatible river glyphs, producing a unique composition through a structured optimization and rendering pipeline.

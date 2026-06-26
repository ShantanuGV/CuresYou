# Technical Details

---

# Introduction

This document describes the internal implementation details of the CurseYou backend.

Unlike the high-level architecture documentation, this guide focuses on how data moves between modules, how the backend is organized, and how the engine performs procedural river composition.

---

# Backend Organization

The backend is divided into several independent modules.

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
    ├── normalizer.py
    ├── ribbon.py
    ├── config.py
    ├── types.py
    └── debug.py
```

Each module is responsible for a single stage of the rendering pipeline.

---

# Core Engine

The heart of the backend is the **river_engine** package.

Its responsibilities include:

* loading metadata
* candidate selection
* optimization
* geometric layout
* stitching
* bridge generation
* image composition
* final rendering

No individual module performs the entire workflow.

Instead, each contributes one processing stage.

---

# Entry Points

## main.py

The command-line entry point.

Responsibilities:

* receive user input
* initialize the pipeline
* invoke the rendering engine
* save generated output

---

## server.py

Provides an HTTP interface for the frontend.

Responsibilities:

* receive API requests
* validate input
* invoke the backend pipeline
* return generated images

The server contains minimal rendering logic.

Most processing occurs inside the engine modules.

---

# Configuration Layer

The configuration module centralizes values used throughout the backend.

Typical configuration includes:

* rendering parameters
* spacing values
* optimization settings
* bridge thresholds
* image processing constants

Centralizing these values simplifies experimentation and maintenance.

---

# Metadata Representation

Every river glyph is represented by structured metadata rather than raw image files alone.

Metadata contains information required during optimization and rendering, including:

* character identity
* geometric information
* river width
* connection points
* image location

The metadata loader converts these records into Python objects before optimization begins.

---

# Candidate Representation

Each character may correspond to multiple river glyphs.

Instead of storing only one candidate, the backend maintains collections of possible representations.

This enables the optimizer to search for the most compatible sequence.

---

# Optimization State

During Beam Search, the optimizer maintains multiple partial solutions simultaneously.

Each state contains:

* processed characters
* selected glyph sequence
* accumulated score

Only the highest-scoring states survive each iteration.

This significantly reduces the search space.

---

# Layout Representation

After optimization, glyphs are assigned spatial positions.

Each positioned glyph contains:

* image reference
* translation offset
* connection information
* rendering order

The layout stage performs geometric computation only.

No image rendering occurs here.

---

# Stitch Representation

Neighbouring glyphs are analysed before rendering.

The stitcher determines:

* whether glyphs connect directly
* whether a bridge is required
* which junction mode should be used

The resulting information is passed to the renderer.

---

# Bridge Objects

When direct connections are not possible, bridge geometry is generated.

Bridge objects contain:

* start point
* end point
* control points
* interpolation geometry

These objects are rendered together with the original river glyphs.

---

# Rendering Layers

Rendering occurs in multiple logical layers.

```text
Background

↓

River Glyphs

↓

Bridges

↓

Overlap Regions

↓

Alpha Blending

↓

Final Composition
```

Separating rendering into layers improves readability and simplifies debugging.

---

# Image Processing

The renderer performs several image-processing operations.

These include:

* mask generation
* Gaussian feathering
* alpha compositing
* overlap handling
* image placement

The renderer never decides which glyphs should be used.

Its responsibility is visual composition.

---

# Geometry Utilities

Shared mathematical operations are centralized in the geometry module.

Examples include:

* point operations
* vector calculations
* path length computation
* angle computation
* angle normalization
* interpolation helpers

Centralizing these functions avoids duplicated implementations.

---

# Data Flow

Throughout execution, data changes form several times.

```text
Text Input

↓

Characters

↓

Metadata Objects

↓

Candidate Collections

↓

Optimized Sequence

↓

Positioned Glyphs

↓

Rendered Layers

↓

Output Image
```

Each transformation enriches the information available for subsequent stages.

---

# Error Handling

The backend is designed so that processing stops gracefully when required data is unavailable.

Examples include:

* missing metadata
* unavailable glyphs
* invalid input
* image loading failures

This prevents later stages from operating on incomplete data.

---

# Extensibility

The modular architecture allows new functionality to be introduced without redesigning the existing pipeline.

Potential extensions include:

* additional datasets
* alternative optimization algorithms
* improved bridge generation
* new rendering techniques
* additional export formats

Because each responsibility is isolated, changes are localized to individual modules.

---

# Developer Notes

When modifying the backend, the recommended workflow is:

1. Update the relevant module.
2. Verify interactions with dependent modules.
3. Test the complete rendering pipeline.
4. Validate generated output.
5. Update documentation if behaviour changes.

Maintaining synchronization between code and documentation ensures long-term maintainability.

---

# Summary

The CurseYou backend is organized as a collection of focused modules that cooperate to transform text into continuous river typography.

By separating metadata loading, optimization, geometry, stitching, and rendering into independent components, the engine remains modular, maintainable, and extensible while producing high-quality procedural compositions.

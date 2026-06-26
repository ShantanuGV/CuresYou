# CurseYou

### *Procedural River Typography Engine*

<p align="center">

*"Transforming real river geometry into procedurally generated typography using computational geometry, graph optimization, and raster compositing."*

</p>

---

<p align="center">







</p>

---

> **CurseYou** is a procedural graphics engine that generates readable words from real river imagery.
>
> Instead of rendering characters from a traditional font, the engine searches a curated database of river glyphs, evaluates thousands of possible combinations, optimizes their continuity using Beam Search, and procedurally stitches them into a single continuous river composition.

Unlike conventional typography systems where every glyph has a fixed position, CurseYou synthesizes each word dynamically. Every output is generated through optimization, geometric alignment, and image composition rather than static font rendering.

---

# Repository Navigation

# Repository Structure

```text
CurseYou/
│
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── SECURITY.md
├── ROADMAP.md
├── CITATION.cff
│
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── ARCHITECTURE.md
│   ├── PIPELINE.md
│   ├── ALGORITHMS.md
│   ├── MATHEMATICS.md
│   ├── DATASET.md
│   ├── TECHNICAL_DETAILS.md
│   ├── API.md
│   ├── PERFORMANCE.md
│   └── FAQ.md
│
├── backend/
│   ├── main.py
│   ├── server.py
│   ├── requirements.txt
│   ├── output.png
│   │
│   ├── river_engine/
│   │   ├── __init__.py
│   │   ├── blending.py
│   │   ├── bridge.py
│   │   ├── config.py
│   │   ├── debug.py
│   │   ├── geometry.py
│   │   ├── layout.py
│   │   ├── metadata_loader.py
│   │   ├── normalizer.py
│   │   ├── optimizer.py
│   │   ├── pipeline.py
│   │   ├── renderer.py
│   │   ├── ribbon.py
│   │   ├── stitcher.py
│   │   └── types.py
│   │
│   ├── tests/
│   └── assets/
│
├── frontend/
│   ├── package.json
│   ├── public/
│   └── src/
│
└── assets/
```

---

# Table of Contents

* Overview
* Why CurseYou?
* Key Features
* Example Output
* System Architecture
* Processing Pipeline
* Core Algorithms
* Mathematical Foundations
* Project Structure
* Installation
* Quick Start
* Configuration
* Performance
* Documentation
* Roadmap
* Contributing
* License

---

# Overview

Typography has traditionally relied on predefined vector glyphs stored inside font files.

CurseYou explores a different approach.

Instead of selecting glyphs from a font, the engine constructs an entirely new composition from extracted river geometries.

Each character exists as multiple river candidates.

The backend then:

1. retrieves all available candidates,
2. evaluates geometric compatibility,
3. searches for the optimal sequence,
4. aligns neighbouring river segments,
5. generates smooth junctions,
6. composites the result into a seamless image.

Every generated word is therefore unique.

---

# Why CurseYou?

Traditional font engines answer a simple question:

> **"Which glyph should represent this letter?"**

CurseYou answers a much more difficult one:

> **"Which combination of real river geometries best represents this entire word while preserving natural river flow?"**

This transforms typography into a constrained optimization problem.

Instead of rendering fonts, the system solves a geometric search problem.

---

# Key Features

## Computational Geometry

* Metadata-driven glyph placement
* River centerline alignment
* Geometric continuity scoring
* Affine transformations
* Bézier bridge generation

---

## Optimization

* Beam Search sequence optimization
* Candidate pruning
* Multi-stage scoring
* Flow consistency analysis
* Junction selection

---

## Rendering

* Alpha compositing
* Procedural stitching
* Dynamic canvas generation
* Layer ordering
* PNG export

---

## Architecture

* Modular backend
* Configurable pipeline
* Metadata indexing
* Independent rendering engine
* Extensible dataset structure

---

# What Makes This Project Different?

Most image generation systems rely on one of the following:

* predefined vector fonts
* neural image generation
* image morphing
* texture synthesis

CurseYou does none of these.

Instead, it combines:

* computational geometry
* graph search
* heuristic optimization
* raster compositing
* procedural layout generation

to construct readable typography directly from river imagery.

---

# High-Level Architecture

```
                         User Input
                              │
                              ▼
                    Input Normalization
                              │
                              ▼
                     Metadata Index Loader
                              │
                              ▼
                   Candidate Retrieval Engine
                              │
                              ▼
                  Beam Search Optimization
                              │
                              ▼
                    Sequence Cost Analysis
                              │
                              ▼
                     Layout Computation
                              │
                              ▼
                     Junction Generation
                              │
                              ▼
                     Bridge Generation
                              │
                              ▼
                     Raster Composition
                              │
                              ▼
                         PNG Export
```

---

# Processing Pipeline

```
Word

↓

Normalize

↓

Load Metadata

↓

Find Candidates

↓

Beam Search

↓

Score Sequence

↓

Compute Layout

↓

Generate Bridges

↓

Alpha Blending

↓

Final Render
```

---

# Mathematical Foundations

CurseYou combines concepts from several computer science disciplines.

| Area                   | Purpose                |
| ---------------------- | ---------------------- |
| Computational Geometry | River alignment        |
| Graph Search           | Candidate optimization |
| Beam Search            | Sequence selection     |
| Affine Geometry        | Glyph placement        |
| Bézier Curves          | Bridge generation      |
| Image Processing       | Alpha compositing      |
| Raster Graphics        | Final rendering        |
| Heuristic Optimization | Cost minimization      |

A detailed mathematical explanation is available in:

```
docs/MATHEMATICS.md
```

---

# Documentation

Complete technical documentation is included inside the `docs/` directory.

| Document             | Description                       |
| -------------------- | --------------------------------- |
| PROJECT_OVERVIEW.md  | Project motivation and objectives |
| ARCHITECTURE.md      | Backend architecture              |
| PIPELINE.md          | Execution pipeline                |
| ALGORITHMS.md        | Search and rendering algorithms   |
| MATHEMATICS.md       | Mathematical derivations          |
| DATASET.md           | River glyph dataset               |
| TECHNICAL_DETAILS.md | Internal implementation           |
| API.md               | Python API                        |
| PERFORMANCE.md       | Benchmarks                        |
| FAQ.md               | Frequently asked questions        |

---

# Project Philosophy

CurseYou treats typography as an optimization problem rather than a rendering problem.

Every generated image is the result of searching, evaluating, aligning, and composing real river geometries into a coherent structure.

The engine prioritizes geometric continuity, visual realism, and modular architecture over predefined artistic templates.

---

**Continue Reading →**

The following documentation explores every subsystem in detail, from metadata indexing and Beam Search optimization to Bézier bridge generation, affine transformations, alpha compositing, and rendering internals.

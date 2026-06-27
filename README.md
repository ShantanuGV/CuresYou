# CurseYou

<h3 align="center">
Procedural River Typography Engine
</h3>

<p align="center">
Transforming real river geometry into procedurally generated typography using computational geometry, heuristic optimization, and raster image compositing.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![Documentation](https://img.shields.io/badge/Documentation-Complete-blue)

</p>

---

## 🌐 Live Demo

**Website**

https://curseyou.vercel.app/

---

## Overview

**CurseYou** is a procedural graphics engine that generates readable words from real river imagery.

Instead of rendering characters from a traditional font, the engine searches a curated database of river glyphs, evaluates numerous candidate combinations, optimizes their continuity using **Beam Search**, computes a geometric layout, and procedurally stitches them into a single continuous river composition.

Unlike conventional typography systems where every glyph has a fixed appearance and position, CurseYou constructs every word dynamically.

Each generated image is produced through:

- metadata-driven glyph retrieval
- heuristic optimization
- computational geometry
- affine transformations
- procedural bridge generation
- alpha compositing
- raster rendering

rather than traditional font rendering.

---

# Repository Navigation

## Root Files

| File | Description |
|------|-------------|
| [README.md](README.md) | Project overview and quick start |
| [LICENSE](LICENSE) | MIT License |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |
| [CHANGELOG.md](CHANGELOG.md) | Project history |
| [SECURITY.md](SECURITY.md) | Security policy |
| [ROADMAP.md](ROADMAP.md) | Planned improvements |
| [CITATION.cff](CITATION.cff) | Citation information |

---

## Documentation

| Document | Description |
|----------|-------------|
| [PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) | Introduction and project goals |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture |
| [PIPELINE.md](docs/PIPELINE.md) | Processing pipeline |
| [ALGORITHMS.md](docs/ALGORITHMS.md) | Optimization and rendering algorithms |
| [MATHEMATICS.md](docs/MATHEMATICS.md) | Mathematical foundations |
| [DATASET.md](docs/DATASET.md) | Dataset organization |
| [TECHNICAL_DETAILS.md](docs/TECHNICAL_DETAILS.md) | Internal implementation |
| [API.md](docs/API.md) | Backend API |
| [PERFORMANCE.md](docs/PERFORMANCE.md) | Performance characteristics |
| [FAQ.md](docs/FAQ.md) | Frequently Asked Questions |

---

# Table of Contents

- [Overview](#overview)
- [Why CurseYou?](#why-curseyou)
- [Key Features](#key-features)
- [Example Output](#example-output)
- [System Architecture](#system-architecture)
- [Processing Pipeline](#processing-pipeline)
- [Core Technologies](#core-technologies)
- [Mathematical Foundations](#mathematical-foundations)
- [Backend Modules](#backend-modules)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

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
│   ├── river_engine/
│   ├── tests/
│   └── assets/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
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

Traditional font rendering systems answer a relatively simple question:

> **"Which glyph should represent this character?"**

The glyph already exists inside a font file. The rendering engine simply determines where it should be placed.

CurseYou approaches typography from a fundamentally different perspective.

Instead of asking which glyph should be drawn, it asks:

> **"Which combination of real river geometries best represents this entire word while preserving natural river flow?"**

Every character has multiple possible river representations. Rather than selecting the first available candidate, the backend evaluates many possible combinations, scores their compatibility, computes an optimized sequence using **Beam Search**, and procedurally assembles the final composition.

This transforms typography into a constrained optimization problem instead of a traditional rendering problem.

Every generated image is unique and is computed at runtime.

---

# Key Features

## 🗺️ Data-Driven Rendering

* Real river imagery used as the source dataset
* Metadata-driven glyph retrieval
* Multiple candidates for every character
* Structured JSON metadata
* Extensible asset library

---

## 🧠 Heuristic Optimization

* Beam Search sequence optimization
* Candidate pruning
* Multi-stage scoring
* Connection quality evaluation
* Width consistency analysis
* Flow continuity scoring

---

## 📐 Computational Geometry

* Geometric layout computation
* River centerline alignment
* Affine transformations
* Distance and angle calculations
* Bounding-box computation
* Relative glyph positioning

---

## 🌉 Procedural Stitching

* Automatic junction detection
* Conditional bridge generation
* Bézier curve interpolation
* Seamless transition handling
* Dynamic overlap computation

---

## 🎨 Rendering Engine

* Alpha compositing
* Feather mask generation
* Layered raster rendering
* Dynamic canvas generation
* PNG export
* Modular rendering pipeline

---

## 🏗️ Software Architecture

* Modular backend
* Independent processing stages
* Configurable engine
* Metadata-driven workflow
* Separation of optimization and rendering
* Easily extensible codebase

---

# What Makes This Project Different?

Most typography and image generation systems fall into one of these categories:

| Approach                     | Used by CurseYou |
| ---------------------------- | ---------------- |
| Traditional Vector Fonts     | ❌                |
| SVG Glyph Rendering          | ❌                |
| Neural Image Generation      | ❌                |
| Diffusion Models             | ❌                |
| Image Morphing               | ❌                |
| Texture Synthesis            | ❌                |
| Procedural River Composition | ✅                |

CurseYou introduces a different approach.

Instead of generating images through artificial intelligence or rendering predefined vector glyphs, it constructs typography by procedurally assembling real river geometries.

The backend combines concepts from several computer science disciplines:

* Computational Geometry
* Heuristic Optimization
* Beam Search
* Image Processing
* Raster Graphics
* Procedural Layout Generation

This combination allows the engine to generate continuous river typography without relying on conventional font rendering techniques.

---

# Example Output

The following illustrates the generation process.

```text
Input

CURSEYOU

↓

Retrieve River Glyph Candidates

↓

Beam Search Optimization

↓

Geometric Layout

↓

Bridge Generation

↓

Image Compositing

↓

Continuous River Typography
```

Additional examples:

```text
SHANTANU
        ↓
Procedurally Generated River Typography
```

```text
GOOGLE
        ↓
Procedurally Generated River Typography
```

```text
INDIA
        ↓
Procedurally Generated River Typography
```

> **Tip:** Replace the examples above with screenshots from your project. Showing actual generated results near the top of the README makes the repository much more engaging.

---

# Core Technologies

## Backend

* Python
* Flask
* Pillow (PIL)
* NumPy

---

## Frontend

* React
* Vite
* JavaScript
* CSS

---

## Algorithms

* Beam Search
* Heuristic Candidate Scoring
* Computational Geometry
* Affine Transformations
* Bézier Curve Interpolation

---

## Image Processing

* Alpha Compositing
* Feather Mask Blending
* Raster Rendering
* Dynamic Canvas Generation

---

## Data Representation

* PNG River Glyph Dataset
* JSON Metadata
* Skeleton Images
* Overlay Images
* River Ribbon Assets

---

# Design Philosophy

CurseYou treats typography as a search and optimization problem rather than a font rendering problem.

The engine separates every major responsibility into an independent module:

* Metadata Loading
* Candidate Retrieval
* Optimization
* Layout Computation
* Stitching
* Bridge Generation
* Rendering

This separation improves readability, maintainability, and extensibility while allowing each stage of the pipeline to evolve independently.


---

# System Architecture

The CurseYou backend is designed as a modular rendering engine where each stage performs a single well-defined responsibility. Instead of tightly coupling rendering logic into one large script, the engine separates metadata loading, optimization, geometric layout, stitching, and rendering into independent components.

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
                    Alpha Compositing
                              │
                              ▼
                      PNG Image Export
```

The architecture follows a pipeline-based design where the output of one stage becomes the input of the next. This separation simplifies maintenance, testing, and future improvements.

---

# Processing Pipeline

Every generated image follows the same execution pipeline.

```
User Input

↓

Normalize Text

↓

Load Metadata

↓

Retrieve Candidate Glyphs

↓

Beam Search Optimization

↓

Evaluate Sequence Cost

↓

Compute Geometric Layout

↓

Generate River Bridges

↓

Alpha Blend Junctions

↓

Raster Composition

↓

PNG Export
```

Each stage transforms the data into a richer representation until the final river typography is produced.

---

# Backend Modules

The backend is organized into small, reusable modules.

| Module | Responsibility |
|----------|---------------|
| `metadata_loader.py` | Loads glyph metadata from JSON files |
| `normalizer.py` | Normalizes and validates input text |
| `optimizer.py` | Performs Beam Search optimization |
| `layout.py` | Computes geometric placement of glyphs |
| `geometry.py` | Shared mathematical and geometric utilities |
| `stitcher.py` | Determines how neighbouring glyphs connect |
| `bridge.py` | Generates procedural bridge segments |
| `blending.py` | Performs alpha blending and seam removal |
| `renderer.py` | Renders the final river composition |
| `pipeline.py` | Coordinates the complete rendering workflow |
| `config.py` | Stores configurable engine parameters |
| `ribbon.py` | Handles ribbon generation utilities |
| `debug.py` | Debugging and visualization helpers |
| `types.py` | Shared data structures used across the engine |

Each module has a clearly defined responsibility, making the backend easier to understand and extend.

---

# Mathematical Foundations

CurseYou combines concepts from multiple areas of computer science and mathematics.

| Area | Purpose |
|------|---------|
| Computational Geometry | River alignment and layout computation |
| Beam Search | Candidate sequence optimization |
| Heuristic Optimization | Compatibility scoring |
| Affine Transformations | Translation and rotation of glyphs |
| Bézier Curves | Smooth procedural bridge generation |
| Raster Graphics | Image generation |
| Alpha Compositing | Seamless junction blending |
| Image Processing | Final rendering and export |

Several mathematical models are used throughout the rendering pipeline, including affine transformations, distance calculations, angle normalization, Bézier interpolation, and alpha blending.

A detailed explanation of these concepts is available in:

**📄 [`docs/MATHEMATICS.md`](docs/MATHEMATICS.md)**

---

# Documentation Hub

The repository includes detailed technical documentation for every major subsystem.

| Document | Description |
|----------|-------------|
| 📘 [`PROJECT_OVERVIEW.md`](docs/PROJECT_OVERVIEW.md) | Project motivation and objectives |
| 🏗️ [`ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Complete backend architecture |
| ⚙️ [`PIPELINE.md`](docs/PIPELINE.md) | Rendering pipeline |
| 🧠 [`ALGORITHMS.md`](docs/ALGORITHMS.md) | Beam Search and rendering algorithms |
| 📐 [`MATHEMATICS.md`](docs/MATHEMATICS.md) | Mathematical concepts and formulas |
| 🗂️ [`DATASET.md`](docs/DATASET.md) | River glyph dataset structure |
| 🔬 [`TECHNICAL_DETAILS.md`](docs/TECHNICAL_DETAILS.md) | Internal implementation details |
| 🌐 [`API.md`](docs/API.md) | Backend API documentation |
| 📊 [`PERFORMANCE.md`](docs/PERFORMANCE.md) | Performance characteristics |
| ❓ [`FAQ.md`](docs/FAQ.md) | Frequently Asked Questions |

If you're new to the project, the recommended reading order is:

```
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
DATASET.md
      ↓
TECHNICAL_DETAILS.md
      ↓
API.md
      ↓
PERFORMANCE.md
      ↓
FAQ.md
```

---

# Project Philosophy

CurseYou treats typography as an optimization problem rather than a rendering problem.

Every generated image is the result of searching, evaluating, aligning, and composing real river geometries into a coherent structure.

The engine prioritizes geometric continuity, visual realism, and modular architecture over predefined artistic templates.

---

# Installation

## Prerequisites

Before running CurseYou locally, ensure the following software is installed:

### Backend

- Python 3.10+
- pip

### Frontend

- Node.js 18+
- npm

---

## Clone the Repository

```bash
git clone https://github.com/<your-username>/CurseYou.git
cd CurseYou
```

---

## Backend Setup

Navigate to the backend directory.

```bash
cd backend
```

Create a virtual environment.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required packages.

```bash
pip install -r requirements.txt
```

---

## Frontend Setup

Open a second terminal.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

---

# Quick Start

## Start the Backend Server

```bash
cd backend

python server.py
```

or

```bash
python main.py
```

depending on your workflow.

---

## Start the Frontend

```bash
cd frontend

npm run dev
```

Open the displayed local URL in your browser.

---

# Technologies Used

## Backend

- Python
- Flask
- Pillow (PIL)
- NumPy

---

## Frontend

- React
- Vite
- JavaScript
- CSS

---

## Computer Science Concepts

- Beam Search
- Computational Geometry
- Affine Transformations
- Bézier Curves
- Raster Graphics
- Alpha Compositing
- Heuristic Optimization
- Procedural Rendering

---

# Features

- ✅ Procedural river typography generation
- ✅ Metadata-driven glyph retrieval
- ✅ Beam Search optimization
- ✅ Geometric layout engine
- ✅ Procedural bridge generation
- ✅ Alpha compositing
- ✅ Modular rendering pipeline
- ✅ REST backend
- ✅ React frontend
- ✅ Extensible dataset

---

# Future Improvements

Planned improvements include:

- SVG export support
- Higher-resolution rendering
- Additional river glyph datasets
- Improved optimization heuristics
- Faster rendering pipeline
- Batch word generation
- Interactive editor
- GPU-assisted rendering

See **[ROADMAP.md](ROADMAP.md)** for the complete roadmap.

---

# Contributing

Contributions are welcome.

If you would like to improve CurseYou, please:

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/my-feature
```

3. Commit your changes.

```bash
git commit -m "Add my feature"
```

4. Push the branch.

```bash
git push origin feature/my-feature
```

5. Open a Pull Request.

Please read **[CONTRIBUTING.md](CONTRIBUTING.md)** before submitting a pull request.

---

# Performance

The rendering pipeline is designed around modular processing rather than brute-force search.

Performance depends primarily on:

- Number of input characters
- Candidate glyph count
- Beam width
- Rendering resolution
- Bridge generation complexity

For a detailed discussion, see:

**[docs/PERFORMANCE.md](docs/PERFORMANCE.md)**

---

# Citation

If you use CurseYou in academic research or publications, please cite the project using the information provided in:

**[CITATION.cff](CITATION.cff)**

---

# License

This project is licensed under the **MIT License**.

See **[LICENSE](LICENSE)** for details.

---

# Acknowledgements

CurseYou is an experimental procedural graphics project that combines concepts from computational geometry, heuristic optimization, image processing, and software engineering to explore a new form of typography based on real-world river imagery.

The project demonstrates how natural geographic structures can be transformed into readable typographic compositions through algorithmic processing instead of conventional font rendering.

---

# Documentation

Complete documentation is available in the **docs/** directory.

📘 Project Overview

🏗️ Architecture

⚙️ Pipeline

🧠 Algorithms

📐 Mathematics

🗂️ Dataset

🔬 Technical Details

🌐 API

📊 Performance

❓ FAQ

---

# Project Status

> **Status:** Active Development

The engine is actively evolving with improvements to optimization, rendering quality, dataset expansion, and overall system architecture.

---

<p align="center">

### ⭐ If you found this project interesting, consider giving it a star!

Made with ❤️ using Python, React, Computational Geometry, and Procedural Graphics.

</p>

**Continue Reading →**

The following documentation explores every subsystem in detail, from metadata indexing and Beam Search optimization to Bézier bridge generation, affine transformations, alpha compositing, and rendering internals.

## Keywords

Procedural Typography, River Typography, Computational Geometry,
Beam Search, Procedural Graphics, Image Stitching,
Image Processing, Raster Compositing, GIS,
Satellite Imagery, Generative Typography,
Creative Coding, Algorithmic Design,
Python, React.

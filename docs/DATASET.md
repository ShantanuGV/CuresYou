# Dataset

---

# Introduction

The CurseYou rendering engine is entirely data-driven.

Instead of storing predefined words or complete river typography, the backend stores a collection of individual river glyphs. During rendering, these glyphs are selected, optimized, positioned, and blended to produce a continuous river composition.

The dataset forms the foundation of the rendering engine.

Without it, the optimization and rendering pipeline cannot operate.

---

# Dataset Overview

The dataset is located inside the backend assets directory.

```text
backend/
└── assets/
```

The backend loads all required resources from this directory during runtime. Asset locations are configured through the engine configuration rather than hardcoded paths. :contentReference[oaicite:0]{index=0}

---

# Dataset Structure

The assets directory is organized into several independent components.

```text
assets/
│
├── New_Letters/
│
├── New_Letters_metadata/
│
├── g_river_tile_2/
│
└── output/
```

Each folder serves a different purpose within the rendering pipeline. :contentReference[oaicite:1]{index=1}

---

# Letter Image Dataset

```text
assets/
└── New_Letters/
```

This directory contains the extracted river glyph images used to construct words.

The glyphs are organized alphabetically.

Example

```text
New_Letters/

├── A/
├── B/
├── C/
├── D/
...
├── Y/
└── Z/
```

Each character directory stores multiple river candidates.

Example

```text
A/

a_0.png

a_1.png

Screenshot_...

amazonia_...
```

Having multiple candidates allows the optimizer to choose the most compatible glyph for neighbouring letters instead of using a fixed representation. :contentReference[oaicite:2]{index=2}

---

# Metadata Dataset

```text
assets/
└── New_Letters_metadata/
```

Every river glyph has an associated metadata file.

Metadata is stored as JSON.

Example

```text
A/

a_0.json

a_1.json

Screenshot....

...
```

The metadata is loaded before optimization begins.

Rather than analysing image pixels repeatedly, the backend reads these metadata files and constructs internal glyph objects for the optimization pipeline. 

---

# Metadata Purpose

Each metadata file describes the geometric properties of one river glyph.

The metadata enables the backend to determine:

- river entry point
- river exit point
- average river width
- geometric dimensions
- rendering information
- compatibility with neighbouring glyphs

The optimizer and stitcher rely on this information when selecting and connecting glyphs.

---

# Overlay Images

Many glyphs include an overlay image.

Example

```text
a_0_overlay.png
```

Overlay images preserve additional river information used during rendering and compositing.

These assets improve the visual quality of overlapping regions. :contentReference[oaicite:4]{index=4}

---

# Skeleton Images

Each glyph also contains a skeleton representation.

Example

```text
a_0_skeleton.png
```

Skeleton images represent the extracted river centerline.

These assets are useful for:

- debugging
- geometric analysis
- metadata generation
- visualization

They are not directly displayed in the final rendered output. :contentReference[oaicite:5]{index=5}

---

# River Ribbon Dataset

```text
assets/
└── g_river_tile_2/
```

The engine also contains a reusable river ribbon dataset.

Configuration references include:

```text
final_river_ribbon_2.jpg

tile_manifest.txt
```

These resources support ribbon rendering and texture generation within the backend. :contentReference[oaicite:6]{index=6}

---

# Output Directory

```text
assets/
└── output/
```

Generated river typography is exported to the output directory.

Every rendered image is produced dynamically during execution.

The dataset itself remains unchanged.

---

# Candidate Diversity

One of the strengths of the dataset is candidate diversity.

Instead of storing one glyph per letter,

the dataset stores multiple river representations.

Example

```text
Letter M

↓

m_0

m_1

Screenshot...

Screenshot...

...
```

This diversity enables Beam Search to construct smoother and more natural river words by selecting the most compatible sequence rather than relying on fixed glyphs. :contentReference[oaicite:7]{index=7}

---

# Dataset Workflow

```text
User Input

↓

Characters

↓

Candidate Folder

↓

Metadata Loading

↓

Beam Search

↓

Best Candidate Selection

↓

Rendering
```

Every rendered word begins with the dataset.

---

# Dataset Statistics

The dataset currently contains:

- Multiple glyph candidates for each supported character
- JSON metadata describing geometric properties
- Overlay images for compositing
- Skeleton images for geometric visualization
- River ribbon textures
- Output directory for generated images

The exact number of glyphs per character varies because additional river samples have been collected over time. 

---

# Adding New Glyphs

The dataset is designed to be extensible.

To add a new river glyph:

1. Place the river image in the appropriate character directory.
2. Generate its corresponding metadata file.
3. Include the overlay image if required.
4. Include the skeleton image.
5. Ensure filenames remain consistent across all associated assets.

Once these files are available, the backend can automatically include the new glyph during candidate retrieval.

---

# Dataset Design Principles

The dataset follows several important principles.

## Modular

Every glyph is independent.

No word-level assets are stored.

---

## Metadata Driven

The backend relies on structured metadata instead of analysing raw images during optimization.

---

## Extensible

New river glyphs can be added without modifying the rendering engine.

---

## Reusable

The same glyph may appear in many different generated words depending on the optimization results.

---

# Summary

The CurseYou dataset is a structured collection of river glyph assets that powers the procedural rendering engine.

It consists of:

- River glyph images
- JSON metadata
- Overlay images
- Skeleton images
- River ribbon textures
- Output directory

During execution, the backend loads these resources, evaluates candidate compatibility, computes an optimized sequence, and procedurally assembles them into continuous river typography.

By separating visual assets from rendering logic, the dataset remains scalable, reusable, and easy to extend as new river glyphs are added.

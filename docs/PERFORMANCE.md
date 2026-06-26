# Performance

---

# Introduction

The performance of CurseYou depends on both the optimization stage and the rendering stage.

Unlike traditional font rendering systems, CurseYou performs procedural generation at runtime. Every generated word requires candidate retrieval, optimization, geometric layout, stitching, and image compositing before the final image is produced.

As a result, execution time depends on the complexity of the input rather than simply the number of characters.

---

# Performance Pipeline

```text
                 User Input
                      │
                      ▼
             Metadata Loading
                 (Low Cost)
                      │
                      ▼
           Candidate Collection
                 (Low Cost)
                      │
                      ▼
         Beam Search Optimization
                (Highest Cost)
                      │
                      ▼
           Layout Computation
               (Medium Cost)
                      │
                      ▼
          Bridge Generation
               (Medium Cost)
                      │
                      ▼
         Image Compositing
               (High Cost)
                      │
                      ▼
             PNG Export
               (Low Cost)
```

---

# Performance Characteristics

The overall runtime is influenced by several independent factors.

## 1. Input Length

Longer words require more processing because additional glyphs must be optimized and rendered.

Example

```text
HELLO

↓

5 Glyphs
```

```text
COMPUTATIONAL

↓

13 Glyphs
```

Longer inputs increase:

* optimization work
* layout computation
* bridge generation
* rendering operations

---

## 2. Candidate Count

Each character may have multiple candidate river glyphs.

More candidates provide greater flexibility during optimization but also increase the search space.

For example

```text
A

↓

A₁
A₂
A₃
A₄
A₅
```

The Beam Search optimizer prevents exponential growth by pruning low-quality states.

---

## 3. Beam Search

The optimization stage is the most computationally intensive component.

Instead of evaluating every possible glyph combination, Beam Search limits exploration to the highest-scoring partial solutions.

This dramatically reduces computation while preserving solution quality.

---

## 4. Rendering Resolution

Image composition cost depends directly on output resolution.

Higher resolution images require:

* more pixel operations
* larger masks
* increased alpha blending
* more memory

Rendering time therefore scales with image size.

---

# Stage Cost Analysis

| Processing Stage         | Relative Cost |
| ------------------------ | ------------: |
| Metadata Loading         |           Low |
| Candidate Retrieval      |           Low |
| Beam Search Optimization |          High |
| Layout Computation       |        Medium |
| Junction Evaluation      |           Low |
| Bridge Generation        |        Medium |
| Alpha Blending           |          High |
| PNG Encoding             |           Low |

The optimization and rendering stages dominate total execution time.

---

# Memory Usage

Memory consumption depends primarily on:

* loaded glyph metadata
* candidate collections
* intermediate images
* alpha masks
* output canvas

The backend allocates memory only for the glyphs and buffers required for the current rendering operation.

---

# Optimization Techniques Used

The backend employs several techniques to reduce unnecessary computation.

## Beam Search Pruning

Only the highest-scoring candidate sequences are retained.

Benefits:

* reduced search space
* lower memory usage
* faster optimization

---

## Modular Processing

Each stage operates only on the data it requires.

This minimizes duplicated work and simplifies debugging.

---

## Shared Geometry Utilities

Frequently used mathematical operations are centralized.

This improves maintainability and avoids duplicated implementations.

---

## Conditional Bridge Generation

Bridges are created only when geometric analysis determines they are necessary.

Avoiding unnecessary bridge creation reduces rendering overhead.

---

# Scalability

The backend scales with several independent variables.

| Factor           | Effect                                         |
| ---------------- | ---------------------------------------------- |
| Word Length      | Increases optimization and rendering time      |
| Candidate Count  | Expands optimization search space              |
| Beam Width       | Increases optimization quality and computation |
| Image Resolution | Increases rendering time and memory            |
| Bridge Count     | Adds geometric processing and compositing      |

---

# Potential Optimizations

The modular architecture allows future performance improvements without redesigning the engine.

Possible enhancements include:

* parallel candidate evaluation
* multi-threaded rendering
* metadata caching
* optimized image loading
* GPU-accelerated compositing
* adaptive Beam Width
* lazy asset loading

These improvements can be introduced independently because responsibilities are separated across modules.

---

# Current Design Goals

The current implementation prioritizes:

* correctness
* modularity
* maintainability
* rendering quality

over aggressive low-level optimization.

This design makes the project easier to understand, extend, and debug while still providing efficient procedural rendering.

---

# Performance Summary

The performance of CurseYou is primarily determined by two major components:

1. **Beam Search Optimization**, which selects the most compatible sequence of river glyphs.

2. **Image Rendering**, which blends and composites the selected glyphs into the final output.

By combining Beam Search, modular processing, conditional bridge generation, and efficient image compositing, the backend maintains a practical balance between rendering quality and computational efficiency.

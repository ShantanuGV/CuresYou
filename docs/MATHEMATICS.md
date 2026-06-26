# Mathematics

---

# Introduction

Although CurseYou generates artistic river typography, its backend is built upon several mathematical concepts from computational geometry, image processing, and heuristic optimization.

Rather than relying on machine learning or predefined font rendering, the engine uses geometric relationships between river glyphs to determine how individual letters should be connected and rendered.

This document explains the mathematical principles used throughout the backend implementation.

---

# Mathematical Pipeline

```text
          River Metadata
                 │
                 ▼
        Geometric Analysis
                 │
                 ▼
        Candidate Evaluation
                 │
                 ▼
      Layout Computation
                 │
                 ▼
      Bridge Generation
                 │
                 ▼
       Image Blending
                 │
                 ▼
         Final Rendering
```

---

# Coordinate System

Every river glyph is represented inside a two-dimensional Cartesian coordinate system.

```text
              y
              ▲
              │
              │
              │
──────────────┼──────────────► x
              │
              │
```

Every important location—including entry points, exit points, centerline points, and bridge control points—is represented as a coordinate pair:

[
P=(x,y)
]

---

# Euclidean Distance

Distances between two points are measured using the Euclidean distance formula.

Given two points

[
P_1=(x_1,y_1)
]

and

[
P_2=(x_2,y_2)
]

their distance is

[
d(P_1,P_2)=
\sqrt{
(x_2-x_1)^2+
(y_2-y_1)^2
}
]

The engine uses this measurement to estimate gaps between neighboring river glyphs.

---

# Path Length

Each river centerline consists of multiple connected points.

If

[
P_1,P_2,\ldots,P_n
]

represent the ordered centerline,

its total length is

[
L=
\sum_{i=1}^{n-1}
\left|
P_{i+1}-P_i
\right|
]

This measurement is used by the geometry utilities when analyzing river shapes.

---

# Vector Representation

The direction of a river segment is represented by a vector.

Given

[
P_1
]

and

[
P_2
]

the direction vector is

[
\vec v=
P_2-P_1
]

or

[
\vec v=
(x_2-x_1,;
y_2-y_1)
]

This representation allows the backend to compare river orientations.

---

# Vector Magnitude

The magnitude of a vector is

[
|\vec v|
========

\sqrt{
v_x^2+v_y^2
}
]

The magnitude describes the length of the directional vector.

---

# Angle Computation

River orientation is determined from the vector direction.

For

[
\vec v=(v_x,v_y)
]

the orientation angle is

[
\theta=
\operatorname{atan2}
(v_y,v_x)
]

The use of

[
atan2
]

ensures that the angle is computed correctly in all quadrants.

---

# Angle Difference

Neighboring glyphs should have similar flow directions.

If

[
\theta_1
]

and

[
\theta_2
]

represent two orientations,

their angular difference is

[
\Delta\theta
============

\theta_2-\theta_1
]

The backend normalizes this value into

[
[-180^\circ,;180^\circ]
]

to prevent discontinuities around the circular boundary.

This measurement is used when evaluating glyph compatibility.

---

# Horizontal Progress

Readable words should primarily progress along the horizontal axis.

For two consecutive points

[
P_1
]

and

[
P_2
]

the displacement is

[
dx=x_2-x_1
]

[
dy=y_2-y_1
]

Large vertical movement relative to horizontal movement reduces the horizontality score.

---

# Linearity

The engine evaluates how smoothly neighboring river glyphs continue the overall direction of the word.

Large directional changes reduce the linearity score.

Although the implementation uses heuristic scoring rather than an analytical function, the mathematical objective is to minimize abrupt directional changes.

---

# Width Comparison

Every glyph stores an estimated river width.

Neighboring glyphs are compared to determine whether the transition appears natural.

Given

[
W_1
]

and

[
W_2
]

their width ratio is

[
R=
\frac
{\min(W_1,W_2)}
{\max(W_1,W_2)}
]

A ratio close to

[
1
]

indicates similar river widths.

---

# Connection Evaluation

Two neighboring glyphs are evaluated using several geometric properties.

These include

* orientation difference
* width consistency
* geometric alignment

Rather than relying on a single measurement, multiple heuristics contribute to the overall connection quality.

---

# Candidate Optimization

Suppose every character has

[
C
]

candidate glyphs,

and the input word contains

[
N
]

characters.

An exhaustive search would require

[
C^N
]

possible combinations.

Instead, the optimizer uses Beam Search.

If

[
K
]

represents the Beam Width,

the approximate search complexity becomes

[
O(NKC)
]

which is significantly smaller than exhaustive evaluation.

---

# Affine Translation

After the optimal sequence has been selected,

each glyph is translated into its final canvas position.

If

[
P=(x,y)
]

is a point,

and

[
T=(t_x,t_y)
]

is the translation vector,

the transformed position becomes

[
P'
==

P+T
]

or

[
(x+t_x,;
y+t_y)
]

This operation is used throughout layout computation.

---

# Cubic Bézier Curve

When a bridge must be inserted,

the backend generates a smooth curve using cubic Bézier interpolation.

The curve is defined as

[
B(t)=
(1-t)^3P_0
+
3(1-t)^2tP_1
+
3(1-t)t^2P_2
+
t^3P_3
]

where

[
0\le t\le1
]

and

[
P_0,P_1,P_2,P_3
]

represent the control points.

The resulting curve provides a smooth transition between disconnected river segments.

---

# Gaussian Feather Mask

Visible seams are reduced using Gaussian feather masks.

The Gaussian distribution is

[
G(x)
====

\frac
1
{\sigma\sqrt{2\pi}}
e^{-\frac{x^2}{2\sigma^2}}
]

Applying this function produces gradual transparency instead of sharp image boundaries.

---

# Alpha Blending

Two overlapping images

[
A
]

and

[
B
]

are merged using alpha compositing.

The resulting pixel color is

[
C
=

\alpha A
+
(1-\alpha)B
]

where

[
0\le\alpha\le1
]

This creates smooth transitions between river glyphs.

---

# Under Compositing

Some overlaps require one river to pass beneath another.

The renderer handles these situations by controlling drawing order before alpha blending is applied.

This produces visually consistent crossings.

---

# Bounding Box

The renderer computes a bounding rectangle that completely contains every glyph.

If

[
x_{min},
x_{max},
y_{min},
y_{max}
]

represent the extreme coordinates,

the canvas dimensions become

[
Width
=====

x_{max}-x_{min}
]

[
Height
======

y_{max}-y_{min}
]

The final image is allocated using these dimensions.

---

# Computational Complexity

Approximate computational complexity of major mathematical operations.

| Operation            | Complexity |
| -------------------- | ---------- |
| Distance Computation | O(1)       |
| Angle Computation    | O(1)       |
| Width Comparison     | O(1)       |
| Path Length          | O(n)       |
| Beam Search          | O(NKC)     |
| Layout Computation   | O(n)       |
| Bridge Generation    | O(m)       |
| Alpha Blending       | O(pixels)  |

---

# Summary

CurseYou combines mathematics from multiple disciplines to transform river imagery into readable typography.

The backend makes extensive use of

* Euclidean geometry
* vector mathematics
* path analysis
* angular computation
* heuristic optimization
* affine transformations
* Bézier interpolation
* Gaussian filtering
* alpha compositing

These mathematical foundations allow independent river glyphs to be positioned, connected, blended, and rendered into a continuous river composition while maintaining visual consistency and readability.

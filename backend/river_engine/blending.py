from __future__ import annotations

import cv2
import numpy as np


def feather_mask(mask: np.ndarray, radius: int) -> np.ndarray:
    if radius <= 0:
        return mask.astype(np.float32) / 255.0
    k = radius * 2 + 1
    blurred = cv2.GaussianBlur(mask.astype(np.float32), (k, k), 0)
    return np.clip(blurred / 255.0, 0.0, 1.0)


def alpha_blend(
    base: np.ndarray,
    overlay: np.ndarray,
    mask: np.ndarray,
    offset: tuple[int, int],
) -> np.ndarray:
    x, y = offset
    h, w = overlay.shape[:2]
    bh, bw = base.shape[:2]
    x1 = min(bw, x + w)
    y1 = min(bh, y + h)
    if x >= bw or y >= bh or x1 <= x or y1 <= y:
        return base

    ox0 = max(0, -x)
    oy0 = max(0, -y)
    bx0 = max(0, x)
    by0 = max(0, y)
    bx1 = x1
    by1 = y1
    ox1 = ox0 + (bx1 - bx0)
    oy1 = oy0 + (by1 - by0)

    region = base[by0:by1, bx0:bx1].astype(np.float32)
    over = overlay[oy0:oy1, ox0:ox1].astype(np.float32)
    alpha = mask[oy0:oy1, ox0:ox1]
    if alpha.ndim == 3:
        alpha = alpha[:, :, 0]
    alpha = alpha.astype(np.float32)
    if alpha.max() > 1.0:
        alpha /= 255.0
    alpha = alpha[..., None]
    blended = over * alpha + region * (1.0 - alpha)
    out = base.copy()
    out[by0:by1, bx0:bx1] = np.clip(blended, 0, 255).astype(np.uint8)
    return out


def alpha_under(
    base: np.ndarray,
    overlay: np.ndarray,
    mask: np.ndarray,
    offset: tuple[int, int],
) -> np.ndarray:
    """
    Place overlay beneath existing base content.

    FIXED VERSION:
    - no letter-shape clipping
    - no river-shape cropping
    - full rectangular underlap
    - cinematic collage layering
    """

    x, y = offset

    h, w = overlay.shape[:2]
    bh, bw = base.shape[:2]

    x1 = min(bw, x + w)
    y1 = min(bh, y + h)

    if x >= bw or y >= bh or x1 <= x or y1 <= y:
        return base

    ox0 = max(0, -x)
    oy0 = max(0, -y)

    bx0 = max(0, x)
    by0 = max(0, y)

    bx1 = x1
    by1 = y1

    ox1 = ox0 + (bx1 - bx0)
    oy1 = oy0 + (by1 - by0)

    # existing canvas region
    region = base[
        by0:by1,
        bx0:bx1
    ].astype(np.float32)

    # incoming full rectangular tile
    under = overlay[
        oy0:oy1,
        ox0:ox1
    ].astype(np.float32)

    # IMPORTANT:
    # ignore mask shape entirely
    # only use it optionally for softness
    alpha = mask[
        oy0:oy1,
        ox0:ox1
    ]

    if alpha.ndim == 3:
        alpha = alpha[:, :, 0]

    alpha = alpha.astype(np.float32)

    if alpha.max() > 1.0:
        alpha /= 255.0

    # soften mask influence heavily
    alpha = alpha * 0.15

    alpha = alpha[..., None]

    # rectangular underlap blend
    opacity = 0.72

    blended = (
        under * opacity
        + region * (1.0 - opacity)
    )

    # slight river preservation
    blended = (
        blended * (1.0 - alpha)
        + region * alpha
    )

    out = base.copy()

    out[
        by0:by1,
        bx0:bx1
    ] = np.clip(
        blended,
        0,
        255,
    ).astype(np.uint8)

    return out


def harmonize_color(
    target: np.ndarray,
    reference: np.ndarray,
    mask: np.ndarray,
) -> np.ndarray:
    if target.size == 0 or reference.size == 0:
        return target
    m = mask > 0
    if m.sum() < 32:
        return target
    if m.shape != target.shape[:2]:
        return target
    tgt_lab = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype(np.float32)
    ref_lab = cv2.cvtColor(reference, cv2.COLOR_BGR2LAB).astype(np.float32)
    for c in range(3):
        t_mean = tgt_lab[:, :, c][m].mean()
        r_mean = ref_lab[:, :, c][m].mean()
        tgt_lab[:, :, c] += r_mean - t_mean
    tgt_lab = np.clip(tgt_lab, 0, 255)
    return cv2.cvtColor(tgt_lab.astype(np.uint8), cv2.COLOR_LAB2BGR)


def seamless_paste(
    base: np.ndarray,
    patch: np.ndarray,
    mask: np.ndarray,
    center: tuple[int, int],
) -> np.ndarray:
    if patch.size == 0:
        return base
    h, w = patch.shape[:2]
    if h < 4 or w < 4:
        return alpha_blend(base, patch, mask, (center[0] - w // 2, center[1] - h // 2))

    m = mask.copy()
    if m.ndim == 3:
        m = cv2.cvtColor(m, cv2.COLOR_BGR2GRAY)
    if m.max() <= 1:
        m = (m * 255).astype(np.uint8)

    cx, cy = center
    x = int(cx - w // 2)
    y = int(cy - h // 2)
    try:
        return cv2.seamlessClone(patch, base, m, (cx, cy), cv2.MIXED_CLONE)
    except cv2.error:
        return alpha_blend(base, patch, m, (x, y))


def build_river_mask(points: np.ndarray, shape: tuple[int, int], width: int) -> np.ndarray:
    mask = np.zeros(shape, dtype=np.uint8)
    if len(points) < 2:
        return mask
    pts = np.round(points).astype(np.int32)
    thickness = max(3, int(round(width)))
    cv2.polylines(mask, [pts], False, 255, thickness=thickness)
    k = max(3, thickness // 2 * 2 + 1)
    mask = cv2.dilate(mask, np.ones((k, k), np.uint8), iterations=1)
    return mask


def build_letter_mask(points: np.ndarray, shape: tuple[int, int], width: int) -> np.ndarray:
    mask = build_river_mask(points, shape, max(4, int(round(width * 0.85))))
    return feather_mask(mask, 8)


def build_letter_fill_mask(points: np.ndarray, shape: tuple[int, int]) -> np.ndarray:
    mask = np.zeros(shape, dtype=np.uint8)
    if len(points) >= 3:
        pts = np.round(points).astype(np.int32)
        cv2.fillPoly(mask, [pts], 255)
    elif len(points) >= 1:
        mask = build_river_mask(points, shape, 6)
    return feather_mask(mask, 5)


def build_overlap_mask(
    shape: tuple[int, int],
    center: tuple[int, int],
    radius: int,
) -> np.ndarray:
    mask = np.zeros(shape, dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)
    return feather_mask(mask, max(3, radius // 4))

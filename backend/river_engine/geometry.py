from __future__ import annotations

import math

import cv2
import numpy as np
from scipy.interpolate import splprep, splev


def to_points(arr: list | np.ndarray) -> np.ndarray:
    pts = np.asarray(arr, dtype=np.float64)
    if pts.ndim != 2 or pts.shape[1] != 2:
        raise ValueError("points must be Nx2")
    return pts


def path_length(points: np.ndarray) -> float:
    if len(points) < 2:
        return 0.0
    diffs = np.diff(points, axis=0)
    return float(np.sum(np.linalg.norm(diffs, axis=1)))


def angle_deg(p0: np.ndarray, p1: np.ndarray) -> float:
    dx = float(p1[0] - p0[0])
    dy = float(p1[1] - p0[1])
    return math.degrees(math.atan2(-dy, dx))


def angle_diff(a: float, b: float) -> float:
    d = (a - b + 180.0) % 360.0 - 180.0
    return abs(d)


def bbox_from_points(points: np.ndarray, pad: int = 0) -> tuple[int, int, int, int]:
    if len(points) == 0:
        return 0, 0, 0, 0
    xs = points[:, 0]
    ys = points[:, 1]
    x0 = max(0, int(np.floor(xs.min())) - pad)
    y0 = max(0, int(np.floor(ys.min())) - pad)
    x1 = int(np.ceil(xs.max())) + pad
    y1 = int(np.ceil(ys.max())) + pad
    return x0, y0, x1, y1


def transform_points(
    points: np.ndarray,
    scale: float,
    rotation_deg: float,
    origin: np.ndarray,
    translation: np.ndarray,
) -> np.ndarray:
    if len(points) == 0:
        return points.copy()
    rad = math.radians(rotation_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    centered = points - origin
    scaled = centered * scale
    rot = np.empty_like(scaled)
    rot[:, 0] = scaled[:, 0] * cos_a - scaled[:, 1] * sin_a
    rot[:, 1] = scaled[:, 0] * sin_a + scaled[:, 1] * cos_a
    return rot + origin + translation


def rotate_image(
    image: np.ndarray,
    rotation_deg: float,
    center: tuple[float, float] | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    h, w = image.shape[:2]
    if center is None:
        center = (w / 2.0, h / 2.0)
    matrix = cv2.getRotationMatrix2D(center, rotation_deg, 1.0)
    rotated = cv2.warpAffine(
        image,
        matrix,
        (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT101,
    )
    return rotated, matrix


def apply_affine_to_points(points: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    if len(points) == 0:
        return points.copy()
    ones = np.ones((len(points), 1), dtype=np.float64)
    hom = np.hstack([points, ones])
    out = hom @ matrix.T
    return out


def resample_polyline(points: np.ndarray, count: int) -> np.ndarray:
    if len(points) < 2:
        return points.copy()
    if count <= 2:
        return points[[0, -1]].astype(np.float64)
    lengths = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(points, axis=0), axis=1))])
    total = lengths[-1]
    if total < 1e-6:
        return np.repeat(points[:1], count, axis=0)
    targets = np.linspace(0.0, total, count)
    xs = np.interp(targets, lengths, points[:, 0])
    ys = np.interp(targets, lengths, points[:, 1])
    return np.column_stack([xs, ys])


def smooth_spline(points: np.ndarray, samples: int = 64) -> np.ndarray:
    if len(points) < 4:
        return resample_polyline(points, samples)
    try:
        tck, _ = splprep(points.T, s=len(points) * 2.0, k=3)
        u = np.linspace(0.0, 1.0, samples)
        x, y = splev(u, tck)
        return np.column_stack([x, y])
    except Exception:
        return resample_polyline(points, samples)


def bezier_curve(p0, p1, p2, p3, samples: int = 48) -> np.ndarray:
    t = np.linspace(0.0, 1.0, samples)[:, None]
    omt = 1.0 - t
    pts = (
        omt**3 * p0
        + 3 * omt**2 * t * p1
        + 3 * omt * t**2 * p2
        + t**3 * p3
    )
    return pts


def unit_from_angle(deg: float) -> np.ndarray:
    rad = math.radians(deg)
    return np.array([math.cos(rad), -math.sin(rad)], dtype=np.float64)


def clamp_bbox(
    bbox: tuple[int, int, int, int],
    width: int,
    height: int,
) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = bbox
    x0 = max(0, min(x0, width - 1))
    y0 = max(0, min(y0, height - 1))
    x1 = max(x0 + 1, min(x1, width))
    y1 = max(y0 + 1, min(y1, height))
    return x0, y0, x1, y1

import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..'
        )
    )
)

import cv2
import json
import torch
import numpy as np

from pathlib import Path

from models.multitask_model import RiverMultiTaskModel


# ============================================================
# CUDA SPEED BOOST
# ============================================================

torch.backends.cudnn.benchmark = True


# ============================================================
# CONFIG
# ============================================================

RIVER_IMAGE = "./../assets/g_river_tile_2/final_river_ribbon_2.jpg"

OUTPUT_LETTERS = "./../assets/m_gpt_letters"

OUTPUT_METADATA = "./../assets/m_gpt_river_metadata_2"

HARD_NEGATIVES = "../hard_negatives"

WINDOW_SIZE = 500

STEP_SIZE = 50

ROTATIONS = [0]

MIN_RIVER_PIXELS = 700

MODEL_INPUT_SIZE = 256

CONFIDENCE_THRESHOLD = 0.45

SEGMENT_MIN_PIXELS = 40

SEGMENT_MAX_PIXELS = 90000

MIN_COMPONENTS = 1

MAX_COMPONENTS = 300

SHOW_LIVE = True

LIVE_SCALE = 420

MASK_THRESHOLD = 0.25

AUTO_SAVE = True

SHOW_REJECTS = True


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device(
    'cuda' if torch.cuda.is_available() else 'cpu'
)

print(f"\nUsing Device: {DEVICE}")


# ============================================================
# MODEL
# ============================================================

MODEL_PATH = "./checkpoints/epoch_100.pth"

model = RiverMultiTaskModel()

checkpoint = torch.load(
    MODEL_PATH,
    map_location=DEVICE
)

model.load_state_dict(
    checkpoint['model_state_dict']
)

model = model.to(DEVICE)

model.eval()

print("Model Loaded.")


# ============================================================
# LABEL MAP
# ============================================================

letter_index_to_char = {

    i: chr(ord('a') + i)

    for i in range(26)
}


# ============================================================
# CREATE OUTPUT FOLDERS
# ============================================================

for ch in "abcdefghijklmnopqrstuvwxyz":

    Path(
        f"{OUTPUT_LETTERS}/{ch}"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    Path(
        f"{OUTPUT_METADATA}/{ch}"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

Path(HARD_NEGATIVES).mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# IMAGE UTILS
# ============================================================

class ImageUtils:

    @staticmethod
    def rotate(img, angle):

        h, w = img.shape[:2]

        center = (w // 2, h // 2)

        M = cv2.getRotationMatrix2D(
            center,
            angle,
            1.0
        )

        cos = abs(M[0, 0])
        sin = abs(M[0, 1])

        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))

        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]

        rotated = cv2.warpAffine(
            img,
            M,
            (new_w, new_h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=0
        )

        return rotated


# ============================================================
# BASIC WATER SEGMENTER
# ============================================================

class RiverSegmenter:

    @staticmethod
    def segment(img):

        hsv = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2HSV
        )

        lower = np.array([60, 8, 8])

        upper = np.array([160, 255, 255])

        mask = cv2.inRange(
            hsv,
            lower,
            upper
        )

        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            (5, 5)
        )

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            kernel
        )

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            kernel,
            iterations=2
        )

        return mask


# ============================================================
# PREPROCESS
# ============================================================

def preprocess_image(img):

    resized = cv2.resize(
        img,
        (
            MODEL_INPUT_SIZE,
            MODEL_INPUT_SIZE
        )
    )

    rgb = cv2.cvtColor(
        resized,
        cv2.COLOR_BGR2RGB
    )

    tensor = rgb.astype(np.float32) / 255.0

    tensor = np.transpose(
        tensor,
        (2, 0, 1)
    )

    tensor = torch.tensor(
        tensor,
        dtype=torch.float32
    ).unsqueeze(0)

    return tensor.to(DEVICE)


# ============================================================
# MASK TO POINTS
# ============================================================

def mask_to_points(mask):

    points = np.column_stack(
        np.where(mask > 0)
    )

    result = []

    for p in points:

        y, x = p

        result.append([
            int(x),
            int(y)
        ])

    return result


# ============================================================
# ENTRY EXIT ESTIMATION
# ============================================================

def estimate_entry_exit(mask):

    ys, xs = np.where(mask > 0)

    if len(xs) == 0:

        return [0, 0], [0, 0]

    left_index = np.argmin(xs)

    right_index = np.argmax(xs)

    entry = [
        int(xs[left_index]),
        int(ys[left_index])
    ]

    exit = [
        int(xs[right_index]),
        int(ys[right_index])
    ]

    return entry, exit


# ============================================================
# SEGMENT QUALITY FILTER
# ============================================================

def validate_mask(mask):

    nonzero = cv2.countNonZero(mask)

    if nonzero < SEGMENT_MIN_PIXELS:
        return False

    if nonzero > SEGMENT_MAX_PIXELS:
        return False

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask)

    components = num_labels - 1

    if components < MIN_COMPONENTS:
        return False

    if components > MAX_COMPONENTS:
        return False

    return True


# ============================================================
# CREATE OVERLAY
# ============================================================

def create_overlay(
    original,
    mask
):

    mask = cv2.resize(
        mask,
        (
            original.shape[1],
            original.shape[0]
        )
    )

    mask = (
        mask * 255
    ).astype(np.uint8)

    heatmap = cv2.applyColorMap(
        mask,
        cv2.COLORMAP_JET
    )

    overlay = cv2.addWeighted(
        original,
        0.75,
        heatmap,
        0.45,
        0
    )

    return overlay


# ============================================================
# LIVE VIEW
# ============================================================

def show_live(
    crop,
    overlay,
    mask,
    predicted_letter,
    confidence,
    x,
    y,
    valid_mask
):

    if not SHOW_LIVE:
        return

    crop_small = cv2.resize(
        crop,
        (LIVE_SCALE, LIVE_SCALE)
    )

    overlay_small = cv2.resize(
        overlay,
        (LIVE_SCALE, LIVE_SCALE)
    )

    mask_vis = (mask * 255).astype(np.uint8)

    mask_vis = cv2.cvtColor(
        mask_vis,
        cv2.COLOR_GRAY2BGR
    )

    mask_vis = cv2.resize(
        mask_vis,
        (LIVE_SCALE, LIVE_SCALE)
    )

    top = np.hstack([
        crop_small,
        overlay_small,
        mask_vis
    ])

    canvas = np.zeros(
        (
            top.shape[0] + 140,
            top.shape[1],
            3
        ),
        dtype=np.uint8
    )

    canvas[:top.shape[0]] = top

    status = "ACCEPTED" if valid_mask else "REJECTED"

    cv2.putText(
        canvas,
        f"Prediction: {predicted_letter}",
        (20, canvas.shape[0] - 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        canvas,
        f"Confidence: {confidence:.4f}",
        (20, canvas.shape[0] - 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.putText(
        canvas,
        f"X={x}  Y={y}",
        (550, canvas.shape[0] - 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    color = (0, 255, 0) if valid_mask else (0, 0, 255)

    cv2.putText(
        canvas,
        status,
        (1000, canvas.shape[0] - 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        3
    )

    cv2.imshow(
        "River Data Miner",
        canvas
    )

    cv2.waitKey(1)


# ============================================================
# SAVE SAMPLE
# ============================================================

def save_sample(
    crop,
    predicted_letter,
    confidence,
    mask,
    angle,
    x,
    y
):

    letter_folder = os.path.join(
        OUTPUT_LETTERS,
        predicted_letter
    )

    metadata_folder = os.path.join(
        OUTPUT_METADATA,
        predicted_letter
    )

    filename = (
        f"{predicted_letter}_"
        f"{x}_{y}_"
        f"{angle}_"
        f"{int(confidence * 10000)}"
    )

    image_path = os.path.join(
        letter_folder,
        filename + ".png"
    )

    metadata_path = os.path.join(
        metadata_folder,
        filename + ".json"
    )

    cv2.imwrite(
        image_path,
        crop
    )

    entry_point, exit_point = estimate_entry_exit(
        mask
    )

    river_points = mask_to_points(mask)

    metadata = {

        "image": image_path.replace(
            "../",
            ""
        ),

        "letter": predicted_letter,

        "confidence": float(confidence),

        "entry_point": entry_point,

        "exit_point": exit_point,

        "rotation_angle": angle,

        "scan_position": [x, y],

        "contains_readable_letter": True,

        "contains_extended_flow": True,

        "river_points": river_points,

        "letter_points": river_points
    }

    with open(metadata_path, 'w') as f:

        json.dump(
            metadata,
            f,
            indent=4
        )

    print(
        f"[SAVE] "
        f"{predicted_letter} "
        f"{confidence:.4f}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("\nLoading River Image...")

    river = cv2.imread(RIVER_IMAGE)

    if river is None:

        print("Could not load river image.")

        exit()

    h, w = river.shape[:2]

    print(f"River Size: {w} x {h}")

    saved = 0

    rejected = 0

    total_scanned = 0

    # ========================================================
    # SLIDING WINDOW
    # ========================================================

    for y in range(
        0,
        h - WINDOW_SIZE,
        STEP_SIZE
    ):

        for x in range(
            0,
            w - WINDOW_SIZE,
            STEP_SIZE
        ):

            total_scanned += 1

            if total_scanned % 50 == 0:

                print(
                    f"Scanned: {total_scanned} | "
                    f"Saved: {saved} | "
                    f"Rejected: {rejected}"
                )

            crop = river[
                y:y + WINDOW_SIZE,
                x:x + WINDOW_SIZE
            ]

            if crop.size == 0:
                continue

            # ====================================================
            # BASIC WATER FILTER
            # ====================================================

            water_mask = RiverSegmenter.segment(
                crop
            )

            river_pixels = cv2.countNonZero(
                water_mask
            )

            if river_pixels < MIN_RIVER_PIXELS:
                continue

            # ====================================================
            # ROTATION SEARCH
            # ====================================================

            for angle in ROTATIONS:

                rotated_crop = ImageUtils.rotate(
                    crop,
                    angle
                )

                tensor = preprocess_image(
                    rotated_crop
                )

                with torch.no_grad():

                    outputs = model(tensor)

                # ================================================
                # LETTER PREDICTION
                # ================================================

                logits = outputs['class_logits']

                probs = torch.softmax(
                    logits,
                    dim=1
                )

                confidence, predicted = torch.max(
                    probs,
                    dim=1
                )

                confidence = confidence.item()

                predicted_letter = letter_index_to_char[
                    predicted.item()
                ]

                # ================================================
                # CONFIDENCE FILTER
                # ================================================

                if confidence < CONFIDENCE_THRESHOLD:
                    continue

                # ================================================
                # SEGMENTATION
                # ================================================

                mask = outputs['segmentation'][0][0]

                mask = torch.sigmoid(mask)

                mask = mask.cpu().numpy()

                mask = (
                    mask > MASK_THRESHOLD
                ).astype(np.uint8)

                # ================================================
                # CLEAN MASK
                # ================================================

                kernel = np.ones(
                    (3, 3),
                    np.uint8
                )

                mask = cv2.morphologyEx(
                    mask,
                    cv2.MORPH_OPEN,
                    kernel
                )

                mask = cv2.morphologyEx(
                    mask,
                    cv2.MORPH_CLOSE,
                    kernel
                )

                # ================================================
                # VALIDATION
                # ================================================

                valid_mask = validate_mask(mask)

                # ================================================
                # OVERLAY
                # ================================================

                overlay = create_overlay(
                    rotated_crop,
                    mask
                )

                # ================================================
                # LIVE VIEW
                # ================================================

                show_live(
                    rotated_crop,
                    overlay,
                    mask,
                    predicted_letter,
                    confidence,
                    x,
                    y,
                    valid_mask
                )

                # ================================================
                # SAVE GOOD
                # ================================================

                if valid_mask:

                    if AUTO_SAVE:

                        save_sample(
                            rotated_crop,
                            predicted_letter,
                            confidence,
                            mask,
                            angle,
                            x,
                            y
                        )

                    saved += 1

                # ================================================
                # SAVE BAD
                # ================================================

                else:

                    rejected += 1

                    if SHOW_REJECTS:

                        print(
                            f"[REJECT] "
                            f"{predicted_letter} "
                            f"{confidence:.4f}"
                        )

                    hard_path = os.path.join(
                        HARD_NEGATIVES,
                        f"reject_{x}_{y}_{angle}.png"
                    )

                    cv2.imwrite(
                        hard_path,
                        rotated_crop
                    )

    print(f"\nFinished.")

    print(f"Total Windows Scanned: {total_scanned}")

    print(f"Saved Samples: {saved}")

    print(f"Rejected Samples: {rejected}")

    cv2.destroyAllWindows()
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
import random
import numpy as np
import gradio as gr

from PIL import Image

from models.multitask_model import RiverMultiTaskModel


# ============================================
# DEVICE
# ============================================

DEVICE = torch.device(
    'cuda' if torch.cuda.is_available() else 'cpu'
)

print(f'Using device: {DEVICE}')


# ============================================
# PATHS
# ============================================

MODEL_PATH = './checkpoints/epoch_100.pth'

LETTERS_DIR = './../assets/letters'


# ============================================
# LABEL MAP
# ============================================

letter_index_to_char = {
    i: chr(ord('a') + i)
    for i in range(26)
}


# ============================================
# LOAD MODEL
# ============================================

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


# ============================================
# LOAD ALL DATASET IMAGES
# ============================================

all_images = []

for root, dirs, files in os.walk(LETTERS_DIR):

    for file in files:

        if file.lower().endswith(
            ('.jpg', '.png', '.jpeg')
        ):

            all_images.append(
                os.path.join(root, file)
            )

print(f'Total Images Found: {len(all_images)}')


# ============================================
# GLOBAL VARIABLES
# ============================================

current_image_path = None
current_prediction = None
current_confidence = None


# ============================================
# IMAGE PREPROCESS
# ============================================

def preprocess_image(image_path):

    image = cv2.imread(image_path)

    original = image.copy()

    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    resized = cv2.resize(
        image,
        (256, 256)
    )

    tensor = resized.astype(np.float32) / 255.0

    tensor = np.transpose(
        tensor,
        (2, 0, 1)
    )

    tensor = torch.tensor(
        tensor,
        dtype=torch.float32
    ).unsqueeze(0)

    return tensor.to(DEVICE), original


# ============================================
# CLEAN OVERLAY
# ============================================

def create_overlay(original, mask):

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

    overlay = original.copy()

    river_pixels = mask > 0

    overlay[river_pixels] = (

        0.6 * overlay[river_pixels]

        + 0.4 * np.array([0, 0, 255])

    )

    return overlay.astype(np.uint8)


# ============================================
# GROUND TRUTH OVERLAY
# ============================================

def create_ground_truth_overlay(
    image_path,
    original
):

    json_path = image_path.replace(
        'letters',
        'river_metadata_2'
    )

    json_path = os.path.splitext(
        json_path
    )[0] + '.json'

    if not os.path.exists(json_path):
        return original

    with open(json_path, 'r') as f:
        metadata = json.load(f)

    h, w = original.shape[:2]

    gt_mask = np.zeros(
        (h, w),
        dtype=np.uint8
    )

    points = np.array(
        metadata['river_points'],
        dtype=np.int32
    )

    cv2.polylines(
        gt_mask,
        [points],
        False,
        255,
        thickness=15
    )

    heatmap = cv2.applyColorMap(
        gt_mask,
        cv2.COLORMAP_HOT
    )

    overlay = cv2.addWeighted(
        original,
        0.7,
        heatmap,
        0.3,
        0
    )

    return overlay


# ============================================
# DATASET PREDICTION
# ============================================

def next_prediction():

    global current_image_path
    global current_prediction
    global current_confidence

    current_image_path = random.choice(
        all_images
    )

    tensor, original = preprocess_image(
        current_image_path
    )

    with torch.no_grad():

        outputs = model(tensor)

    # ========================================
    # LETTER PREDICTION
    # ========================================

    logits = outputs['class_logits']

    probs = torch.softmax(
        logits,
        dim=1
    )

    confidence, predicted = torch.max(
        probs,
        dim=1
    )

    predicted_letter = letter_index_to_char[
        predicted.item()
    ]

    current_prediction = predicted_letter

    current_confidence = confidence.item()

    # ========================================
    # SEGMENTATION
    # ========================================

    mask = outputs['segmentation'][0][0]

    mask = torch.sigmoid(mask)

    mask = mask.cpu().numpy()

    mask = (
        mask > 0.5
    ).astype(np.float32)

    # ========================================
    # OVERLAYS
    # ========================================

    overlay = create_overlay(
        original,
        mask
    )

    ground_truth_overlay = (
        create_ground_truth_overlay(
            current_image_path,
            original
        )
    )

    # ========================================
    # RGB CONVERSION
    # ========================================

    original_rgb = cv2.cvtColor(
        original,
        cv2.COLOR_BGR2RGB
    )

    overlay_rgb = cv2.cvtColor(
        overlay,
        cv2.COLOR_BGR2RGB
    )

    gt_overlay_rgb = cv2.cvtColor(
        ground_truth_overlay,
        cv2.COLOR_BGR2RGB
    )

    # ========================================
    # ACTUAL LABEL
    # ========================================

    actual_letter = os.path.basename(
        os.path.dirname(current_image_path)
    )

    info = f'''
Actual Letter: {actual_letter}

Predicted Letter: {predicted_letter}

Confidence: {current_confidence:.4f}

Device: {DEVICE}

Image:
{current_image_path}
'''

    return (

        Image.fromarray(original_rgb),

        Image.fromarray(overlay_rgb),

        Image.fromarray(gt_overlay_rgb),

        info
    )


# ============================================
# RANDOM IMAGE PREDICTION
# ============================================

def predict_uploaded_image(input_image):

    global current_prediction
    global current_confidence

    image = np.array(input_image)

    original = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2BGR
    )

    resized = cv2.resize(
        image,
        (256, 256)
    )

    tensor = resized.astype(np.float32) / 255.0

    tensor = np.transpose(
        tensor,
        (2, 0, 1)
    )

    tensor = torch.tensor(
        tensor,
        dtype=torch.float32
    ).unsqueeze(0).to(DEVICE)

    with torch.no_grad():

        outputs = model(tensor)

    # ========================================
    # LETTER PREDICTION
    # ========================================

    logits = outputs['class_logits']

    probs = torch.softmax(
        logits,
        dim=1
    )

    confidence, predicted = torch.max(
        probs,
        dim=1
    )

    predicted_letter = letter_index_to_char[
        predicted.item()
    ]

    current_prediction = predicted_letter

    current_confidence = confidence.item()

    # ========================================
    # SEGMENTATION
    # ========================================

    mask = outputs['segmentation'][0][0]

    mask = torch.sigmoid(mask)

    mask = mask.cpu().numpy()

    mask = (
        mask > 0.85
    ).astype(np.float32)

    # ========================================
    # OVERLAY
    # ========================================

    overlay = create_overlay(
        original,
        mask
    )

    overlay_rgb = cv2.cvtColor(
        overlay,
        cv2.COLOR_BGR2RGB
    )

    info = f'''
Uploaded Image Prediction

Predicted Letter: {predicted_letter}

Confidence: {current_confidence:.4f}

Device: {DEVICE}
'''

    return (

        Image.fromarray(image),

        Image.fromarray(overlay_rgb),

        info
    )


# ============================================
# SAVE FEEDBACK
# ============================================

def save_feedback(
    letter_correct,
    letter_accuracy,
    river_correct,
    river_accuracy
):

    feedback = {

        'image': current_image_path,

        'predicted_letter': current_prediction,

        'confidence': current_confidence,

        'letter_correct': letter_correct,

        'letter_accuracy': letter_accuracy,

        'river_correct': river_correct,

        'river_accuracy': river_accuracy
    }

    os.makedirs(
        '../feedback',
        exist_ok=True
    )

    feedback_path = (
        '../feedback/review_data.json'
    )

    # ========================================
    # LOAD OLD FEEDBACK
    # ========================================

    if os.path.exists(feedback_path):

        with open(feedback_path, 'r') as f:
            data = json.load(f)

    else:
        data = []

    # ========================================
    # APPEND FEEDBACK
    # ========================================

    data.append(feedback)

    with open(feedback_path, 'w') as f:

        json.dump(
            data,
            f,
            indent=4
        )

    # ========================================
    # HARD EXAMPLES
    # ========================================

    if (
        not letter_correct
        or not river_correct
        or letter_accuracy < 50
        or river_accuracy < 50
    ):

        os.makedirs(
            '../hard_examples',
            exist_ok=True
        )

        hard_example_path = os.path.join(
            '../hard_examples',
            os.path.basename(
                current_image_path
            )
        )

        image = cv2.imread(
            current_image_path
        )

        cv2.imwrite(
            hard_example_path,
            image
        )

    return 'Feedback Saved Successfully'


# ============================================
# GRADIO UI
# ============================================

with gr.Blocks() as demo:

    gr.Markdown(
        '# River Typography AI — Review System'
    )

    # ========================================
    # RANDOM IMAGE TESTING
    # ========================================

    gr.Markdown(
        '## Upload Random River Image'
    )

    with gr.Row():

        upload_input = gr.Image(
            type='pil',
            label='Upload River Image'
        )

        upload_overlay = gr.Image(
            label='Prediction Overlay'
        )

    upload_info = gr.Textbox(
        label='Upload Prediction'
    )

    upload_button = gr.Button(
        'Predict Uploaded Image'
    )

    # ========================================
    # DATASET TESTING
    # ========================================

    gr.Markdown(
        '## Dataset Review System'
    )

    with gr.Row():

        original_output = gr.Image(
            label='Raw Image'
        )

        overlay_output = gr.Image(
            label='AI River Prediction'
        )

        gt_output = gr.Image(
            label='Human River Annotation'
        )

    prediction_info = gr.Textbox(
        label='Prediction Info'
    )

    # ========================================
    # FEEDBACK CHECKBOXES
    # ========================================

    with gr.Row():

        letter_correct = gr.Checkbox(
            label='Letter Detection Correct'
        )

        river_correct = gr.Checkbox(
            label='River Detection Correct'
        )

    # ========================================
    # ACCURACY SLIDERS
    # ========================================

    with gr.Row():

        letter_accuracy = gr.Slider(
            0,
            100,
            value=50,
            label='Letter Accuracy %'
        )

        river_accuracy = gr.Slider(
            0,
            100,
            value=50,
            label='River Accuracy %'
        )

    # ========================================
    # BUTTONS
    # ========================================

    with gr.Row():

        next_button = gr.Button(
            'Next Image'
        )

        save_button = gr.Button(
            'Save Feedback'
        )

    save_status = gr.Textbox(
        label='Status'
    )

    # ========================================
    # EVENTS
    # ========================================

    upload_button.click(

        fn=predict_uploaded_image,

        inputs=upload_input,

        outputs=[

            upload_input,

            upload_overlay,

            upload_info
        ]
    )

    next_button.click(

        fn=next_prediction,

        outputs=[

            original_output,

            overlay_output,

            gt_output,

            prediction_info
        ]
    )

    save_button.click(

        fn=save_feedback,

        inputs=[

            letter_correct,

            letter_accuracy,

            river_correct,

            river_accuracy
        ],

        outputs=save_status
    )


# ============================================
# LAUNCH
# ============================================

demo.launch()
import os
import json
import cv2
import torch
import numpy as np

from torch.utils.data import Dataset


class RiverDataset(Dataset):
    def __init__(self,
                 letters_dir="../assets/letters",
                 metadata_dir="../assets/river_metadata_2",
                 image_size=256):

        self.letters_dir = letters_dir
        self.metadata_dir = metadata_dir
        self.image_size = image_size

        self.samples = []

        self.letter_to_index = {
            chr(ord('a') + i): i
            for i in range(26)
        }

        self._load_dataset()

    def _load_dataset(self):

        for letter_folder in os.listdir(self.metadata_dir):

            folder_path = os.path.join(
                self.metadata_dir,
                letter_folder
            )

            if not os.path.isdir(folder_path):
                continue

            for file_name in os.listdir(folder_path):

                if not file_name.endswith('.json'):
                    continue

                json_path = os.path.join(folder_path, file_name)

                with open(json_path, 'r') as f:
                    metadata = json.load(f)

                image_path = os.path.join(
                                '..',
                                metadata['image']
                            )

                self.samples.append({
                    'image_path': image_path,
                    'metadata': metadata
                })

        print(f"Loaded {len(self.samples)} samples")

    def __len__(self):
        return len(self.samples)

    def _create_mask(self, points, shape):

        mask = np.zeros(shape[:2], dtype=np.uint8)

        if len(points) < 2:
            return mask

        pts = np.array(points, dtype=np.int32)

        cv2.polylines(
            mask,
            [pts],
            isClosed=False,
            color=255,
            thickness=5
        )

        return mask

    def __getitem__(self, idx):

        sample = self.samples[idx]

        image_path = sample['image_path']
        metadata = sample['metadata']

        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(
                f"Failed to load image: {image_path}"
            )

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image = cv2.resize(
            image,
            (self.image_size, self.image_size)
        )

        river_mask = self._create_mask(
            metadata['river_points'],
            image.shape
        )

        letter_mask = self._create_mask(
            metadata['letter_points'],
            image.shape
        )

        river_mask = cv2.resize(
            river_mask,
            (self.image_size, self.image_size)
        )

        letter_mask = cv2.resize(
            letter_mask,
            (self.image_size, self.image_size)
        )

        image = image.astype(np.float32) / 255.0

        image = np.transpose(image, (2, 0, 1))

        label = self.letter_to_index[
            metadata['letter'].lower()
        ]

        return {
            'image': torch.tensor(image, dtype=torch.float32),
            'label': torch.tensor(label, dtype=torch.long),
            'river_mask': torch.tensor(
                river_mask / 255.0,
                dtype=torch.float32
            ).unsqueeze(0),

            'letter_mask': torch.tensor(
                letter_mask / 255.0,
                dtype=torch.float32
            ).unsqueeze(0)
        }


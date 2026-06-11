import cv2
import matplotlib.pyplot as plt

from datasets.dataset import RiverDataset


def visualize_sample(index=0):

    dataset = RiverDataset()

    sample = dataset[index]

    image = sample['image'].numpy().transpose(1, 2, 0)

    river_mask = sample['river_mask'][0].numpy()
    letter_mask = sample['letter_mask'][0].numpy()

    metadata = sample['metadata']

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(image)
    plt.title(f"Letter: {metadata['letter']}")

    plt.subplot(1, 3, 2)
    plt.imshow(river_mask, cmap='gray')
    plt.title("River Mask")

    plt.subplot(1, 3, 3)
    plt.imshow(letter_mask, cmap='gray')
    plt.title("Letter Mask")

    plt.show()


if __name__ == '__main__':
    visualize_sample(0)

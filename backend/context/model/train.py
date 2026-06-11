import os
import torch
import torch.nn as nn

from tqdm import tqdm
from torch.utils.data import DataLoader

from datasets.dataset import RiverDataset
from models.multitask_model import RiverMultiTaskModel


def train():

    device = torch.device(
        'cuda' if torch.cuda.is_available() else 'cpu'
    )

    print(f"Using device: {device}")

    dataset = RiverDataset()

    dataloader = DataLoader(
        dataset,
        batch_size=16,
        shuffle=True
    )

    model = RiverMultiTaskModel()

    model = model.to(device)

    classification_loss_fn = nn.CrossEntropyLoss()

    segmentation_loss_fn = nn.BCELoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=1e-4
    )

    epochs = 100

    os.makedirs('model/checkpoints', exist_ok=True)

    for epoch in range(epochs):

        model.train()

        total_loss = 0

        progress = tqdm(dataloader)

        for batch in progress:

            images = batch['image'].to(device)
            labels = batch['label'].to(device)
            river_masks = batch['river_mask'].to(device)

            outputs = model(images)

            cls_loss = classification_loss_fn(
                outputs['class_logits'],
                labels
            )

            seg_loss = segmentation_loss_fn(
                outputs['segmentation'], river_masks)

            loss = cls_loss + seg_loss

            optimizer.zero_grad()

            loss.backward()

            optimizer.step()

            total_loss += loss.item()

            progress.set_description(
                f"Epoch {epoch+1} Loss: {loss.item():.4f}"
            )

        avg_loss = total_loss / len(dataloader)

        print(f"Epoch {epoch+1} Average Loss: {avg_loss:.4f}")

        checkpoint_path = (
            f"model/checkpoints/epoch_{epoch+1}.pth"
        )

        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': avg_loss
        }, checkpoint_path)

        print(f"Saved checkpoint: {checkpoint_path}")


if __name__ == '__main__':
    train()

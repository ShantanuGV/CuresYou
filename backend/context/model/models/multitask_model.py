import torch
import torch.nn as nn

from torchvision.models import efficientnet_b0


class RiverMultiTaskModel(nn.Module):

    def __init__(self, num_classes=26):
        super().__init__()

        backbone = efficientnet_b0(weights='DEFAULT')

        self.encoder = backbone.features

        self.pool = nn.AdaptiveAvgPool2d(1)

        self.classifier = nn.Sequential(
            nn.Linear(1280, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )

        self.segmentation_head = nn.Sequential(
            nn.Conv2d(1280, 512, 3, padding=1),
            nn.ReLU(),

            nn.ConvTranspose2d(512, 256, 2, stride=2),
            nn.ReLU(),

            nn.ConvTranspose2d(256, 128, 2, stride=2),
            nn.ReLU(),

            nn.ConvTranspose2d(128, 64, 2, stride=2),
            nn.ReLU(),

            nn.ConvTranspose2d(64, 32, 2, stride=2),
            nn.ReLU(),

            nn.ConvTranspose2d(32, 1, 2, stride=2),
            nn.Sigmoid()
        )

    def forward(self, x):

        features = self.encoder(x)

        pooled = self.pool(features)

        pooled = pooled.view(pooled.size(0), -1)

        class_logits = self.classifier(pooled)

        segmentation = self.segmentation_head(features)

        return {
            'class_logits': class_logits,
            'segmentation': segmentation
        }

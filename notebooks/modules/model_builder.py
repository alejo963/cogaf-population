"""
Contains PyTorch model code to instantiate a TinyVGG model.
"""
import torch
from torch import nn

from math import floor


def out_shape_calc(in_shape: int, kernel_size: int, stride: int = 1, padding: int = 0, dilation: int = 1) -> int:
    """Utility function to calculate the output shape of a convolution or pooling layer"""
    return floor((in_shape + 2 * padding - dilation * (kernel_size - 1) - 1) / stride + 1)


class BaseModel(nn.Module):
    """Simple Linear model for baseline comparison"""

    def __init__(self, in_features: int, hidden_units: int, out_features: int):
        super().__init__()
        self.linear_stack = nn.Sequential(
            nn.Linear(in_features, hidden_units),
            nn.ReLU(),
            nn.Linear(hidden_units, hidden_units),
            nn.ReLU(),
            nn.Linear(hidden_units, out_features)
        )

    def forward(self, x: torch.Tensor):
        return self.linear_stack(x)


class ConvModel(nn.Module):
    """Basic convolution model.

    Args:
    in_channels: An integer indicating number of input channels.
    in_length: An integer indicating the input length  
    hidden_units: An integer indicating number of hidden units between layers.
    output_shape: An integer indicating number of output units.
    """

    def __init__(self, in_channels: int, in_length: int, hidden_units: int, out_shape: int):
        super().__init__()
        self.conv_stack_1 = nn.Sequential(
            nn.Conv1d(in_channels=in_channels,
                      out_channels=hidden_units,
                      kernel_size=3,
                      stride=1,
                      padding=1),
            nn.ReLU(),
            nn.Conv1d(in_channels=hidden_units,
                      out_channels=hidden_units,
                      kernel_size=2,
                      stride=1,
                      padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2)
        )
        length = out_shape_calc(in_shape=in_length,
                                kernel_size=3, stride=1, padding=1)
        length = out_shape_calc(in_shape=length,
                                kernel_size=2, stride=1, padding=1)
        length = out_shape_calc(in_shape=length, kernel_size=2, stride=2)
        self.conv_stack_2 = nn.Sequential(
            nn.Conv1d(in_channels=hidden_units,
                      out_channels=hidden_units,
                      kernel_size=3,
                      stride=1,
                      padding=1),
            nn.ReLU(),
            nn.Conv1d(in_channels=hidden_units,
                      out_channels=hidden_units,
                      kernel_size=2,
                      stride=1,
                      padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2)
        )
        length = out_shape_calc(
            in_shape=length, kernel_size=3, stride=1, padding=1)
        length = out_shape_calc(in_shape=length,
                                kernel_size=2, stride=1, padding=1)
        length = out_shape_calc(in_shape=length, kernel_size=2, stride=2)
        print(length)
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_features=hidden_units*length,
                      out_features=out_shape)
        )

    def forward(self, x: torch.Tensor):
        x = self.conv_stack_1(x)
        # print(f"Conv layer 1 out shape; {x.shape}")
        x = self.conv_stack_2(x)
        # print(f"Conv layer 2 out shape; {x.shape}")
        x = self.classifier(x)
        # print(f"classifier out shape; {x.shape}")
        return x

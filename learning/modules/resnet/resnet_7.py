import torch
from torch import nn as nn

from learning.modules.blocks import ResBlockStrided, ResBlock


class ResNet7(torch.nn.Module):
    def __init__(self, channels, down_pad=False):
        super(ResNet7, self).__init__()

        down_padding = 0
        if down_pad:
            down_padding = 1

        # inchannels, outchannels, kernel size
        self.conv1 = nn.Conv2d(3, channels, 3, stride=2, padding=down_padding)

        self.block1 = ResBlockStrided(channels, stride=2, down_padding=down_padding)
        self.block2 = ResBlockStrided(channels, stride=2, down_padding=down_padding)
        self.block3 = ResBlockStrided(channels, stride=1, down_padding=down_padding)

        self.res_norm = nn.InstanceNorm2d(channels)

    def init_weights(self):
        self.block1.init_weights()
        self.block2.init_weights()
        self.block3.init_weights()

        torch.nn.init.kaiming_uniform(self.conv1.weight)
        self.conv1.bias.data.fill_(0)

    def forward(self, input):
        x = self.conv1(input)
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)
        x = self.res_norm(x)
        return x
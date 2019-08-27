# -*- coding: utf-8 -*-
"""
Created on Thu May  9 15:07:11 2019

@author: huanghao
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class band_conv(nn.Module):
    """
    normal conv with BN
    conv ==> BN ==> LeakyReLU 
    """
    def __init__(self, in_f=32, out_f=32, keenel_size=3):
        super(band_conv, self).__init__()
        self.conv = nn.Conv1d(in_f, out_f, 3, padding=1)
        self.bn = nn.BatchNorm1d(out_f, affine=True, momentum=0.99, eps=1e-3)
        self.leakyRelu = nn.LeakyReLU(0.1)
    
    def forward(self, x_in, x_concat=None):
        x = self.conv(x_in)
        x = self.bn(x)
        x = self.leakyRelu(x)
        
        if x_concat is not None:
            diff = x_concat.shape[2] - x.shape[2]
            x = F.pad(x, (diff//2, diff-diff//2), mode="replicate")
            
            x = torch.cat([x, x_concat], dim=1)
        return x
    

class band_conv_down(nn.Module):
    """
    normal conv with maxpool
    conv ==> BN ==> LeakyReLU
    """
    def __init__(self):
        super(band_conv_down, self).__init__()
        self.conv = nn.Conv1d(32, 32, 3, padding=1)
        self.bn = nn.BatchNorm1d(32)
        self.leakyRelu = nn.LeakyReLU(0.1)
        self.pool = nn.MaxPool1d(2)
        
    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.leakyRelu(x)
        x = self.pool(x)
        return x


class band_conv_up(nn.Module):
    """
    normal conv with upsampling
    conv ==> BN ==> LeakyReLU ==> concat ==> conv ==> BN ==> LeakyReLU ==> upsampling
    """
    def __init__(self, concat=True):
        super(band_conv_up, self).__init__()
        self.conv1 = band_conv()
        self.conv2 = band_conv(in_f=64 if concat else 32)
        self.up = nn.Upsample(scale_factor=2)
        
    def forward(self, x_in, x_concat=None):
        x = self.conv1(x_in, x_concat)
        x = self.conv2(x)
        x = self.up(x)
        return x


class band_conv_out(nn.Module):
    """
    the last conv layer
    """
    def __init__(self, in_f):
        super(band_conv_out, self).__init__()
        self.conv = nn.Conv1d(in_f, 1, 1)
        
    def forward(self, x):
        x = self.conv(x)
        return x

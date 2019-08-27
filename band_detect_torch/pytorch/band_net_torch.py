# -*- coding: utf-8 -*-
"""
Created on Thu May  9 15:09:17 2019

@author: huanghao
"""

import torch
import torch.nn as nn
from torch.nn import functional as F

from band_net_parts import band_conv
from band_net_parts import band_conv_down
from band_net_parts import band_conv_out
from band_net_parts import band_conv_up

from torchsummary import summary


class band_net(nn.Module):
    """
    band_net wrapper
    """
    def __init__(self):
        super(band_net, self).__init__()
        self.input = band_conv(in_f=1, out_f=32)
        self.down = band_conv_down()
        self.up = band_conv_up(concat=True)
        self.up2 = band_conv_up(concat=False)
        self.conv1 = band_conv(in_f=32, out_f=32)
        self.conv2 = band_conv(in_f=64, out_f=32)
        self.conv3 = band_conv(in_f=32, out_f=2)
        self.out = band_conv_out(2)
        
    def forward(self, x_in):
        x_in = self.input(x_in)    # 8192 * 1
        x1 = self.down(x_in)     # 4096 * 32
        x2 = self.down(x1)       # 2048 * 32
        x3 = self.down(x2)       # 1024 * 32
        x4 = self.down(x3)       # 512 * 32
        x5 = self.down(x4)       # 256 * 32
        x6 = self.down(x5)       # 128 * 32
        x7 = self.down(x6)       # 64 * 32
        
        x8 = self.up2(x7)         # 128 * 32
        x9 = self.up(x8, x6)     # 256 * 32
        x10 = self.up(x9, x5)    # 512 * 32
        x11 = self.up(x10, x4)   # 1024 * 32
        x12 = self.up(x11, x3)   # 2048 * 32
        x13 = self.up(x12, x2)   # 4096 * 32
        x14 = self.up(x13, x1)   # 8192 * 32
        x = self.conv1(x14, x_in)  # 8192 * 64
        x = self.conv2(x)          # 8192 * 32
        x = self.conv1(x)          # 8192 * 32
        
        x = self.conv3(x)       # 8192 * 2
        x = self.out(x)         # 8192 * 1
        
        return torch.sigmoid(x)
    
    
class band_net_s(nn.Module):
    """
    band_net wrapper
    """
    def __init__(self):
        super(band_net_s, self).__init__()
        self.input = band_conv(in_f=1, out_f=32)
        self.down1 = band_conv_down()
        self.down2 = band_conv_down()
        self.down3 = band_conv_down()
        self.down4 = band_conv_down()
        self.down5 = band_conv_down()
        self.down6 = band_conv_down()
        self.down7 = band_conv_down()
        self.up1 = band_conv_up(concat=False)
        self.up2 = band_conv_up(concat=True)
        self.up3 = band_conv_up(concat=True)
        self.up4 = band_conv_up(concat=True)
        self.up5 = band_conv_up(concat=True)
        self.up6 = band_conv_up(concat=True)
        self.up7 = band_conv_up(concat=True)
        self.conv1 = band_conv(in_f=32, out_f=32)
        self.conv2 = band_conv(in_f=64, out_f=32)
        self.conv3 = band_conv(in_f=32, out_f=32)
        self.conv4 = band_conv(in_f=32, out_f=2)
        self.out = band_conv_out(2)
        
    def forward(self, x_in):
        x_in = self.input(x_in)    # 8192 * 1
        x1 = self.down1(x_in)     # 4096 * 32
        x2 = self.down2(x1)       # 2048 * 32
        x3 = self.down3(x2)       # 1024 * 32
        x4 = self.down4(x3)       # 512 * 32
        x5 = self.down5(x4)       # 256 * 32
        x6 = self.down6(x5)       # 128 * 32
        x7 = self.down7(x6)       # 64 * 32
        
        x8 = self.up1(x7)         # 128 * 32
        x9 = self.up2(x8, x6)     # 256 * 32
        x10 = self.up3(x9, x5)    # 512 * 32
        x11 = self.up4(x10, x4)   # 1024 * 32
        x12 = self.up5(x11, x3)   # 2048 * 32
        x13 = self.up6(x12, x2)   # 4096 * 32
        x14 = self.up7(x13, x1)   # 8192 * 32
        
        x = self.conv1(x14, x_in)  # 8192 * 64
        x = self.conv2(x)          # 8192 * 32
        x = self.conv3(x)          # 8192 * 32
        
        x = self.conv4(x)       # 8192 * 2
        x = self.out(x)         # 8192 * 1
        
        return torch.sigmoid(x)

    
if __name__ == "__main__":
    net = band_net_s()
    
    inputs = torch.randn(1, 1, 8192)
    concat = torch.randn(1, 32, 8192)
    out = net(inputs).data.numpy()
    
    summary(net, (1, 25288), device="cpu")
    
    d = net.state_dict()
    k = list(d.keys())
    
    w = {}
    i = 0
    keys = []
    for item in d:
#        layer_name, layer_type, _ = item.split(".")
        layer = item[:len(item)-item[::-1].find(".")-1]
        if layer not in keys:
            keys.append(layer)
            w[layer] = []
        w[layer].append(item)
    
#    w_torch = []
#    cnt = 0
#    for child in net.children():
#        cnt += 1
#        if isinstance(child, (band_conv, band_conv_down, band_conv_out)):
#            for m in child.children():
#                if isinstance(m, nn.Sequential):
#                    for mm in m.children():
#                        if isinstance(mm, nn.Conv1d):
#                            w_torch.append(["conv1d", mm.state_dict()])
#                        if isinstance(mm, nn.BatchNorm1d):
#                            w_torch.append(["batchnorm1d", mm.state_dict()])
#                else:
#                    if isinstance(m, nn.Conv1d):
#                        w_torch.append(["conv1d", mm.state_dict()])
#                    if isinstance(m, nn.BatchNorm1d):
#                        w_torch.append(["batchnorm1d", mm.state_dict()])
#        
#        elif isinstance(child, band_conv_up):
#            for _m in child.children():
#                if isinstance(_m, band_conv):
#                    for m in _m.children():
#                        if isinstance(m, nn.Sequential):
#                            for mm in m.children():
#                                if isinstance(mm, nn.Conv1d):
#                                    w_torch.append(["conv1d", mm.state_dict()])
#                                if isinstance(mm, nn.BatchNorm1d):
#                                    w_torch.append(["batchnorm1d", mm.state_dict()])
#                        else:
#                            if isinstance(mm, nn.Conv1d):
#                                w_torch.append(["conv1d", mm.state_dict()])
#                            if isinstance(mm, nn.BatchNorm1d):
#                                w_torch.append(["batchnorm1d", mm.state_dict()])
#                else:
#                    if isinstance(_m, nn.Conv1d):
#                        w_torch.append(["conv1d", mm.state_dict()])
#                    if isinstance(_m, nn.BatchNorm1d):
#                        w_torch.append(["batchnorm1d", mm.state_dict()])
                
        
#        elif isinstance(child, band_conv_out):
#            for m in child.children():
#                if isinstance(m, nn.Conv1d):
#                        w_torch.append(["conv1d", mm.state_dict()])
#        else:
#            print(child)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#        for m in child.children():
#            if isinstance(m, nn.Sequential):
#                for mm in m.children():
#                    if isinstance(mm, nn.Conv1d):
#                        w_torch.append(["conv1d", mm.state_dict()])
#                    if isinstance(mm, nn.BatchNorm1d):
#                        w_torch.append(["batchnorm1d", mm.state_dict()])
#            else:
#                if isinstance(mm, nn.Conv1d):
#                    w_torch.append(["conv1d", mm.state_dict()])
# -*- coding: utf-8 -*-


import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import numpy as np
import matplotlib.pyplot as plt

from .band_net import band_net
from .preprocessing import data_preprocessing

def _result_smooth(data_origin, y_pred, rr, **kwargs):
    threshold = 2.5
    least_band_width = 7
    if "threshold" in kwargs.keys():
        threshold = kwargs["threshold"]
    if "least_band_width" in kwargs.keys():
        least_band_width = kwargs["least_band_width"]
        
    if y_pred[0] > 0:
        y_pred = np.insert(y_pred, 0, 0)
    if y_pred[-1] > 0:
        y_pred = np.insert(y_pred, len(y_pred), 0)    
    
    y_ = y_pred[:-1] - y_pred[1:]
    
    start = np.array(np.where(y_ < 0)[0]) + rr
    end = np.array(np.where(y_ > 0)[0]) + rr
    
    labels = np.array([item for item in (
            zip(start, end)
            ) if item[1] - item[0] > least_band_width
    ])        
    
    true_labels = []
        
    for x, y in labels:
        w = y - x
        smooth = np.round(w/7).astype(np.int)
        k1 = np.mean(data_origin[x+smooth : y-smooth])
                
        min_w = (w * 0.2).astype(np.int)
        # 越界处理
        if x - min_w < 0:
            left_min = np.min(data_origin[: x+1])
        else:
            left_min = np.min(data_origin[x-min_w : x+1])
            
        if y + min_w > len(data_origin) + 1:
            right_min = np.min(data_origin[y-1 :])
        else:
            right_min = np.min(data_origin[y-1 : y+min_w])
        
        min_v = np.min([left_min, right_min])
        delta = k1 - min_v
        if delta > threshold:
            true_labels.append([x, w, min_v, delta])
            
    return true_labels


def _plot_res(data, labels, save_path=None, show=True, data_type="max"):
    data_min = np.min(data)
    data_max = np.max(data)
    data_dx = data_max - data_min
    
    fig = plt.figure(figsize=(18, 9))
    ax = fig.add_subplot(111)
    ax.plot(data, lw=0.5, color="k")
    
    ax.set_title(f"result-{data_type}", fontsize=12)
    ax.set_xlim((0, len(data)))
    ax.set_ylim((data_min - data_dx/2, data_max + data_dx/2))
    
    for x, w, min_v, delta in labels:
        p = plt.Rectangle((x, min_v), w, delta, 
                          color = "r", alpha = 0.3, fill=1, lw=0.5)
        ax.add_patch(p)
    
    fig.tight_layout()
    if save_path is not None:
        plt.savefig(save_path)
        
    if not show:
        plt.close()
        
def result_smooth(data_origin, y_pred, rr, **kwargs):
    threshold = 2.5
    least_band_width = 7
    if "threshold" in kwargs.keys():
        threshold = kwargs["threshold"]
    if "least_band_width" in kwargs.keys():
        least_band_width = kwargs["least_band_width"]
        
    if y_pred[0] > 0:
        y_pred = np.insert(y_pred, 0, 0)
    if y_pred[-1] > 0:
        y_pred = np.insert(y_pred, len(y_pred), 0)    
    
    y_ = y_pred[:-1] - y_pred[1:]
    
    start = np.array(np.where(y_ < 0)[0]) + rr
    end = np.array(np.where(y_ > 0)[0]) + rr
    
    labels = np.array([item for item in (
            zip(start, end)
            ) if item[1] - item[0] > least_band_width
    ])        
    
    true_labels = []
        
    for x, y in labels:
        w = y - x
        smooth = np.round(w/7).astype(np.int)
        k1 = np.mean(data_origin[x+smooth : y-smooth])
                
        min_w = (w * 0.2).astype(np.int)
        # 越界处理
        if x - min_w < 0:
            left_min = np.min(data_origin[: x+1])
        else:
            left_min = np.min(data_origin[x-min_w : x+1])
            
        if y + min_w > len(data_origin) + 1:
            right_min = np.min(data_origin[y-1 :])
        else:
            right_min = np.min(data_origin[y-1 : y+min_w])
        
        if k1 - left_min > threshold or k1 - right_min > threshold:
            true_labels.append([x, y])
            
    return true_labels


def plot_res(data, labels, save_path=None, show=True):
    data_min = np.min(data)
    data_max = np.max(data)
    data_dx = data_max - data_min
    
    fig = plt.figure(figsize=(18, 9))
    ax = fig.add_subplot(111)
    ax.plot(data, lw=0.5, color="k")
    
    ax.set_title("result", fontsize=12)
    ax.set_xlim((0, len(data)))
    ax.set_ylim((data_min - data_dx/2, data_max + data_dx/2))
    
    for x, y in labels:
        w = y - x
        p = plt.Rectangle((x, data_min), w, data_dx, 
                          color = "r", alpha = 0.3, fill=1, lw=0.5)
        ax.add_patch(p)
    
    fig.tight_layout()
    if save_path is not None:
        plt.savefig(save_path)
        
    if not show:
        plt.close()

## new_shape_data 20181012
def new_shape_data(data, input_len=8192, pad=128, overlap=128):
    length = len(data)
    each_length = input_len - pad - overlap
    n = length//each_length
    mean_data = np.mean(data)
    
    if length > n * each_length: #判断是否刚好整除
        tmp = data[n*each_length:] #最后一段
        v1 = 0
        v2 = 0
        if np.mean(tmp[:100]) < 1.1*mean_data:
            v1 = np.min(tmp)
        if np.mean(tmp[-100:]) < 1.1*mean_data:
            v2 = np.min(tmp)
            
        data_ = np.pad(tmp, (pad//2, input_len - len(tmp) - pad//2), mode="constant", constant_values=(v1, v2))
        
    data_ = np.reshape(data_, (1, input_len, 1))
    
    if length - n*each_length >= overlap:  # 保证每一段都会向后重叠overlap长度
        tmp_data = data[: n*each_length + overlap]
    else:
        tmp_data = np.pad(data, (0, n*each_length + overlap - length), mode="minimum")
    
    for i in range(n):
        tmp = tmp_data[i*each_length : (i+1)*each_length + overlap]
        
        v1 = 0
        v2 = 0
        if np.mean(tmp[:100]) < 1.1*mean_data:
            v1 = np.min(tmp)
        if np.mean(tmp[-100:]) < 1.1*mean_data:
            v2 = np.min(tmp)
            
        tmp = np.reshape(np.pad(tmp, (pad//2, pad//2), mode="constant", constant_values=(v1, v2)), (1, input_len, 1))
        data_ = np.concatenate((data_, tmp), axis = 0)
        
    p = np.array(list(range(1, len(data_))) + [0]) #将排在最开始的最后一个移至最后
    x_test = data_[p]
    
    return x_test


def re_shape_pred(pred, data, input_len=8192, pad=128, overlap=128):
    length = len(data)
    each_length = input_len - pad - overlap
    
    tmp_pred = []
    pred = np.reshape(pred, (pred.shape[0], input_len))
                
    pred = np.where(pred >= 0.5, 1, 0)
    
    for i in range(len(pred)):
        if i == len(pred) - 1:
            tmp = pred[-1][pad//2 : len(data) - i*each_length + pad//2]
            tmp = np.pad(tmp, (i*each_length, 0), mode="constant", constant_values=(0, 0))
        else:
            tmp = pred[i][pad//2 : input_len-pad//2]

            if i*each_length + len(tmp) > length:
                tmp = tmp[:length - i*each_length - len(tmp)]
                tmp = np.pad(tmp, (i*each_length, 0), mode="constant", constant_values=(0, 0))
                print(len(tmp))
            else:
                tmp = np.pad(tmp, (i*each_length, length - i*each_length - len(tmp)), mode="constant", constant_values=(0, 0))
        
        tmp_pred.append(tmp)
    
    true_pred = np.sum(tmp_pred, 0)
    true_pred = np.where(true_pred>0, 1, 0)
    
    return true_pred


class DetectApp():
    pad=128
    overlap=64
    def __init__(self, model_path):
        self.model = band_net(input_length=None)
        self.model.load_weights(model_path)
    
    def detect(self, data_origin, plot=True, save_path=None, 
               shape=False, show=True, threshold=5):
        true_data, rr = data_preprocessing(data_origin)
        
        if not shape:
            x_test = np.reshape(true_data, (1, -1, 1))
            pred = self.model.predict(x_test, verbose=0)
            true_pred = np.where(pred>0.5, 1, 0)
            
        else:
            x_test = new_shape_data(true_data, pad=self.pad, overlap=self.overlap)
            pred = self.model.predict(x_test, verbose=0)
            true_pred = re_shape_pred(pred, true_data, pad=self.pad, overlap=self.overlap)
        
        true_labels = result_smooth(data_origin, true_pred.flatten(), rr, 
                                    threshold=threshold,
                                    least_band_width=7)
        
        if plot:
            plot_res(data_origin, true_labels, save_path=save_path, show=show)
            plt.show()
        return true_labels
    
    
class DetectApp_t():
    pad=128
    overlap=64
    def __init__(self, model_path, plot=False):
        self.model = band_net(input_length=None)
        self.model.load_weights(model_path)
        self.plot_flg = plot
    
    def detect(self, data_origin, plot=True, save_path=None, 
               shape=False, show=True, threshold=5, data_type="max"):
        self.plot_flg = plot
        true_data, rr = data_preprocessing(data_origin)
        
        if not shape:
            x_test = np.reshape(true_data, (1, -1, 1))
            pred = self.model.predict(x_test, verbose=0)
            true_pred = np.where(pred>0.5, 1, 0)
            
        else:
            x_test = new_shape_data(true_data, pad=self.pad, overlap=self.overlap)
            pred = self.model.predict(x_test, verbose=0)
            true_pred = re_shape_pred(pred, true_data, pad=self.pad, overlap=self.overlap)
        
        true_labels = _result_smooth(data_origin, true_pred.flatten(), rr, 
                                    threshold=threshold,
                                    least_band_width=7)
        
        if self.plot_flg:
            _plot_res(data_origin, true_labels, save_path=save_path, show=show, data_type=data_type)
        return true_labels
    
    def show(self):
        if self.plot_flg:
            plt.show()
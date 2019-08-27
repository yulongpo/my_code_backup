# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 09:16:22 2018

@author: huanghao
"""

import numpy as np

def data_preprocessing(data):
    data = np.array(data)
    o_data = data = (data - np.min(data)) / (np.max(data) - np.min(data))
    data = np.copy(o_data)
    d1 = data[1:] - data[:-1]
    d1 = d1 + (np.abs(d1) - d1)/2
    d1 = np.concatenate(([d1[0]], d1))
    data = data - d1    
    threshold = (np.max(data) - np.min(data))/22  #阈值随最大差值改变！！！！
    
#    print("(np.max(data) - np.min(data)) =", (np.max(data) - np.min(data)))
    
    h=int(200*np.std(data))
    tmp = np.concatenate((data, np.zeros(h) + data[-1]))
    #求局部均值
    ave = np.array([np.mean(tmp[i:i+h]) for i in range(len(tmp) - h)])

    
    start = np.where((data - ave + threshold) < 0)[0][0]
#    plt.figure()
#    plt.plot(data)
#    plt.plot(ave - threshold)
#    plt.axvline(start, color="r", linewidth=2)
    
    data = np.array(list(reversed(data)))
    tmp = np.concatenate((data, np.zeros(h) + data[-1]))
    #求局部均值
    ave = np.array([np.mean(tmp[i:i+h]) for i in range(len(tmp) - h)])
    

    
    end = len(data) - np.where((data - ave + threshold) < 0)[0][0]
#    plt.axvline(end, color="r", linewidth=2)
 
#    data = np.array(list(reversed(data)))
    data = o_data[start:end]
    data = (data - np.min(data)) / (np.max(data) - np.min(data))
    
    return data, start


def data_debug(data):
    data = np.array(data)
    data = (data - np.min(data)) / (np.max(data) - np.min(data))
#    d1 = data[1:] - data[:-1]
#    d1 = d1 + (np.abs(d1) - d1)/2
#    d1 = np.concatenate(([d1[0]], d1))
#    data = data - d1
    
    threshold = (np.max(data) - np.min(data))/22  #阈值随最大差值改变！！！！
        
    h = int(200*np.std(data))
    tmp = np.concatenate((data, np.zeros(h) + data[-1]))
    #求局部均值
    ave = np.array([np.mean(tmp[i:i+h]) for i in range(len(tmp) - h)])

    
    start = np.where((data - ave + threshold) < 0)[0][0]
    plt.figure(figsize=(12, 8))
    plt.plot(data)
    plt.plot(ave - threshold)
    plt.axvline(start, color="r", linewidth=2, alpha=0.3)
    
    data = np.array(list(reversed(data)))
    tmp = np.concatenate((data, np.zeros(h) + data[-1]))
    #求局部均值
    ave = np.array([np.mean(tmp[i:i+h]) for i in range(len(tmp) - h)])
    
    end = len(data) - np.where((data - ave + threshold) < 0)[0][0]
    plt.axvline(end, color="r", linewidth=2, alpha=0.3)
 
    data = np.array(list(reversed(data)))
    data = data[start:end]
    data = (data - np.min(data)) / (np.max(data) - np.min(data))
    
    return data, start


def data_finit(data):
    o_data = np.copy(data)
    
    
    d1 = np.abs(data[1:] - data[:-1])    
    d1 = np.concatenate(([d1[0]], d1))
    
    plt.figure(figsize=(12, 8))
    plt.plot(o_data, label="o_data")
    plt.plot(d1)
    plt.plot(o_data - d1)


if __name__ == "__main__":
    from getData import read_new_data, read_origin_data
    import os
    import matplotlib.pyplot as plt
    
    threshold_ = 2  #标准阈值3dB
    dataPath = "../true_data"
#    dataPath = "../d1"
    
    for file in os.listdir(dataPath)[7:]:
        data, _ = read_origin_data(os.path.join(dataPath, file))
#        data, _, __, dis = read_h5_data(normalize=False)
        data = np.array(data)
        
        o_data = np.copy(data)
        d1 = data[1:] - data[:-1]
        d1 = d1 + (np.abs(d1) - d1)/2
        d1 = np.concatenate(([d1[0]], d1))
        data = o_data - d1
#        plt.figure(figsize=(12, 8))
#        plt.plot(o_data, label="o_data")
#        plt.plot(d1)
#        plt.plot(data)
        
        res = data_debug(data)
#        plt.figure()
#        plt.plot(data)
#        plt.title([h, res])
#        plt.axvline(res[-1], color="r")
#        plt.axvline(res[-1] + len(res[0]), color="r")
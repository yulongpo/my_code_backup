# -*- coding: utf-8 -*-
"""
Created on 

@author: huanghao
"""


import numpy as np
from scipy.signal import resample
import os

from .waveFileCapture import waveDataScaning
import __init__


class DataCapture(waveDataScaning):
    """从真实样本中取出数据"""
    def __init__(self):
        super(DataCapture, self).__init__()
        
    def get_data_labels(self, file_name):
        """
        * 从真实样本中取出数据
        
        Parameters
        ----------
        * @file_name: str, 样本名字（路径+名字）
        
        * Returns: [data_ave, label_ave, data_max, label_max]
        ----------
        * @data_ave: list[tuple]，平均谱数据
        * @label_ave: list[list with shape [T, 2]], 平均谱载波标签（起止点）
        * @data_max: list[tuple]，最大谱数据
        * @label_max: list[list with shape [T, 2]], 最大谱载波标签（起止点）
        """
        self.dataPath = file_name
        self.dataUpdate()
        
        data_ave = []
        data_max = []
        label_ave = []
        label_max = []
        
        for i in range(self.allSigFrame):
            self.curSigFrame = i + 1
            self.readCurFrame()
            data_ave.append(self.dataAve)
            data_max.append(self.dataMax)
            
            _label_ave = []
            _label_max = []
            for res in self.waveResult:
                # 忽略错误的载波
                if res.midFreq <= self.freqStart or res.midFreq >= self.freqEnd:
                    continue
                
                x1 = np.ceil(((res.midFreq - res.bandWidth/2) -
                              self.freqStart)/self.freqRes).astype(np.int)
                x2 = np.floor(((res.midFreq + res.bandWidth/2) -
                               self.freqStart)/self.freqRes).astype(np.int)
                x1 = np.maximum(x1, 0)
                x2 = np.minimum(x2, self.fftLen//2 - 1)
                
                # TODO: 修改 8 的限制
                if x2 - x1 < 8:
                    continue
                
                if res.waveFitting == 0:  # 通用
                    _label_ave.append([x1, x2])
                    _label_max.append([x1, x2])
                elif res.waveFitting == 1:  # 平均谱
                    _label_ave.append([x1, x2])
                elif res.waveFitting == 2:  # 最大谱
                    _label_max.append([x1, x2])
                    
            label_ave.append(_label_ave)
            label_max.append(_label_max)
            
        return data_ave, label_ave, data_max, label_max


def adjust_start(start, label_start, label_end, **kwargs):
    """
    * 根据标签调整切断起点值
    
    Parameters
    ----------
    * @start: int, 切断起点值且该值一定小于最大载波起点
    * @label_start: ndArray, 标签起点，且已经按从小到大进行排列
    * @label_end: ndArray, 标签终点，且已经按从小到大进行排列
    
    * @Return: int, 调整后的起点值
    """
    assert(np.any(label_start>start))
    
    if "debug" in kwargs.keys():
        debug = kwargs["debug"]  # 调试起点错误信息
    else:
        debug = False
        
    if debug:
        print("start: {:5d} ====".format(start))
    
    index = np.where(label_start > start)[0][0]
    near_gt_start = label_start[index]  # 与start相邻最近的标签起点
    
    # 求与start相邻最近标签终点，当与start相邻最近的标签起点为第一个时，则该终点值为0
    if index == 0:
        near_lt_end = 0  
    else:
        near_lt_end = label_end[index - 1]
        
    try:
        # 当start点落在上述两点之间时，则start即为所求，否则在两点之间随机取一点
        if start <= near_lt_end or start >= near_gt_start:
            if near_lt_end + 1 == near_gt_start - 1:
                start = near_lt_end + 1
            else:
                start = np.random.randint(near_lt_end+1, near_gt_start-1)
        return start
    except ValueError as e:
        print("start Error: {} ==================================".format(e))
        print("index: {}".format(index))
        print("start Error: {} ==================================".format(e))
       

def adjust_end(end, label, data_len, **kwargs):
    """
    * 根据标签调整切断终点值
    
    Parameters
    ----------
    * @end: int, 切断终点
    * @label: ndArray with shape (T, 2), 与data对应的标签数据，且已经按从小到大进行排列
    * @data_len: int, 当前处理的数据长度
    
    * @Return: int, 调整后的终点值
    """
    if "debug" in kwargs.keys():
        debug = kwargs["debug"]  # 调试起点错误信息
    else:
        debug = False
        
    if debug:
        print("end: {:5d} ====".format(end))
    
    _label = np.sort(label.reshape(-1)) 
    
    if end <= _label[1]:  # 终点值小于第一个载波终点时，则取出第一个载波
#        print("=============", end)
        if len(_label) > 2:
            _end = _label[2]
        else:  # 整个宽带只有一个载波
            _end = data_len - 1
        return np.random.randint(_label[1], _end)
    elif end > data_len - 1:  # 终点值大于数据长度，则取到数据结尾
        return data_len
    elif end >= _label[-1]:  # 终点落在最后一个载波终点后
        return end    
    
    # 终点值落在载波中间，此时至少存在一个载波终点大于end
    index = np.where(_label>end)[0][0]
    try:
        if index % 2 == 0:  # end落在两个载波中间
            return end
        else:  # end落在某个载波上
            if index == len(_label) - 1:  # end落在最后一个载波上
                if _label[index] >= data_len - 1:
                    end = data_len - 1
                else:
                    end = np.random.randint(_label[index], data_len-1)
                return end
            else:
                end = np.random.randint(_label[index], _label[index+1])
                return end
    except ValueError as e:
        print("end Error: {} ==================================".format(e))
        print("index: {}".format(index))
        print("end Error: {} ==================================".format(e))
    
    
""" 绑定别名 get_data_labels，无需初始化DataCapture类 """
get_data_labels = DataCapture().get_data_labels

def process_data_labels(data, label, start=None, input_length=8192,
                        least_band_width=8, debug=False):
    """
    * 从原始数据中切取一段数据用来作为训练集，通常该段数据长度大于等于输入长度，且保持所有原始
      载波频带完整，所以需要对该段切取的数据和对应的label进行resample
      
    Parameters
    ----------
    * @data: ndArray with shape (N,), 一个原始的频谱数据
    * @label: ndArray with shape (T, 2), 与data对应的标签数据，且已经按从小到大进行排列
    * @start: int, 切段起点值
    * @input_length: int, 目标输入长度
    * @least_band_widh: int, 可接受的最小带宽点数
    * @debug: bool, 调试
    
    * Returns: [is_least_band_proper, real_data, real_label]
    ----------
    * @is_least_band_proper: bool, resample后最小带宽是否大于可接受的最小带宽点数，
        大于则正常返回数据，否则返回两个空的ndArray
    * @real_data: ndArray with shape(8192, ), 处理后的频谱数据
    * @real_label: ndArray with shape(8192, ), 处理后的用于网络训练的标签
    """
    label_start = label[:, 0]
    label_end = label[:, 1]
    
    least_label_band_width = np.min(label_end - label_start)
    is_least_band_proper = True
    
    if start is None:  # 若起点不指定，则随机生成一个起点
        start = np.random.randint(0, label_start[-1])
    real_start = adjust_start(start, label_start, label_end, debug=False)
    
    end = real_start + input_length
    real_end = adjust_end(end, label, len(data))
    
    scale = 8192/(real_end - real_start)
    if scale*least_label_band_width < least_band_width:
        is_least_band_proper = False
        if debug:
            return is_least_band_proper, np.array([]), np.array([]), real_start, real_end, least_label_band_width
        return is_least_band_proper, np.array([]), np.array([])
    
    real_data = data[real_start : real_end]
    _label_data = np.zeros_like(data)
    for x1, x2 in label:
        _label_data[x1 : x2] += 1
    real_label = _label_data[real_start : real_end]
    
    real_data = resample(real_data, input_length)
    real_data = (real_data - np.min(real_data))/(np.max(real_data) - np.min(data))
    real_label = np.where(resample(real_label, input_length) > 0.5, 1, 0)
    
    if debug:
        return is_least_band_proper, real_data, real_label, real_start, real_end, least_label_band_width
    return is_least_band_proper, real_data, real_label    


def scale_wave_data(data, label, scale=None, least_band_width=8):
    """
    * 数据尺度变换
    
    Parameters
    ----------
    * @data: ndArray like, 频谱数据
    * @label: ndArray with shape (T, 2), 与data对应的标签数据，且已经按从小到大进行排列
    * @least_band_widh: int, 可接受的最小带宽点数
    
    * Returns: 
        scale: float, 最终真实的scale大小
        data: ndArray like, 尺度变换后的频谱数据
    """
    if scale is None:
        # range[0.4, 1.5] eps:0.01
        scale = np.random.randint(40, 150)/100  
        
    label_start = label[:, 0]
    label_end = label[:, 1]
    least_label_band_width = np.min(label_end - label_start)
    
    # 当scale过小时，则选择更大的scale
    while scale*least_label_band_width < least_band_width:
        scale = np.random.randint(int(scale*100), 150)/100
#    print(scale)
    
    resample_length = int(len(data) * scale)
    data_ = resample(data, resample_length)
          
    return data_, scale



""" 
-------------------------------------------------------------------------------
------------------------------- TEST ------------------------------------------
-------------------------------------------------------------------------------
"""

def _test_without_scale(files):
    """
    * 频谱数据不做长度变换
    """
    for file_name in files[:]:
        print(file_name, "-------")
        data_ave, label_ave, data_max, label_max = get_data_labels(file_name)
        
        for i in range(len(data_ave)):
            print("\t\t====  data_ave:{}  ====".format(i))
            data = np.array(data_ave[i])            
            label = np.stack(label_ave[i])
            label = label[np.lexsort(label.T, 0)]
            for xx in range(20):
                ok, _, __, start, end, lw = process_data_labels(data, label, debug=True)
                if ok:
#                    print("\t\t\t{}\t{}\t{}\t{}".format(xx, ok, start, end))
                    pass
                else:
                    print("\t\t\t{}\t{}\t{}\t{}\t{} ====".format(xx, ok, start, end, lw))
        print("\tdata_ave all tested!")
        
        for i in range(len(data_max)):
            print("\t\t====  data_max:{}  ====".format(i))
            data = np.array(data_max[i])            
            label = np.stack(label_max[i])
            label = label[np.lexsort(label.T, 0)]
            for xx in range(20):
                ok, _, __, start, end, lw = process_data_labels(data, label, debug=True)
                if ok:
#                    print("\t\t\t{}\t{}\t{}\t{}".format(xx, ok, start, end))
                    pass
                else:
                    print("\t\t\t{}\t{}\t{}\t{}\t{} ====".format(xx, ok, start, end, lw))
        print("\tdata_max all tested!")
    
    
def _test_with_scale(files, pre_scale=0.4):
    """
    * 频谱数据做长度变换
    """
    for file_name in files[:]:
        print(file_name, "-------")
        data_ave, label_ave, data_max, label_max = get_data_labels(file_name)
        
        for i in range(len(data_ave)):
            print("\t\t====  data_ave:{}  ====".format(i))
            data = np.array(data_ave[i])            
            label = np.stack(label_ave[i])
            label = label[np.lexsort(label.T, 0)]
            data, scale = scale_wave_data(data, label, pre_scale)
            label = (label*scale).astype(np.int)
            for xx in range(10):
                ok, _, __, start, end, lw = process_data_labels(data, label, debug=True)
                if ok:
                    print("\t\t\t{}\t{}\t{}\t{}".format(xx, ok, start, end))
                else:
                    print("\t\t\t{}\t{}\t{}\t{}\t{} ====".format(xx, ok, start, end, lw))
        print("\tdata_ave all tested!")
        
        for i in range(len(data_max)):
            print("\t\t====  data_max:{}  ====".format(i))
            data = np.array(data_max[i])            
            label = np.stack(label_max[i])
            label = label[np.lexsort(label.T, 0)]
            data, scale = scale_wave_data(data, label, pre_scale)
            label = (label*scale).astype(np.int)
            for xx in range(10):
                ok, _, __, start, end, lw = process_data_labels(data, label, debug=True)
                if ok:
                    print("\t\t\t{}\t{}\t{}\t{}".format(xx, ok, start, end))
                else:
                    print("\t\t\t{}\t{}\t{}\t{}\t{} ====".format(xx, ok, start, end, lw))
        print("\tdata_max all tested!")
    
    
    
def _test_bug(files, pre_scale=0.4, log_file=None):
    """
    找出start点调整中的bug
    """
    if log_file is not None:
        if os.path.exists(log_file):
            os.remove(log_file)
        
    file_index = {}
    
    datas = []
    labels = []
    
    for file_name in files:
        data_ave, label_ave, data_max, label_max = get_data_labels(file_name)
        for i in range(len(data_ave)):
            data = np.array(data_ave[i])            
            label = np.stack(label_ave[i])
            label = label[np.lexsort(label.T, 0)]
            
            datas.append(data)
            labels.append(label)
            file_index[len(datas) - 1] = file_name.split("\\")[-1] + "_ave"
            
        for i in range(len(data_max)):
            data = np.array(data_max[i])            
            label = np.stack(label_max[i])
            label = label[np.lexsort(label.T, 0)]
        
            datas.append(data)
            labels.append(label)
            file_index[len(datas) - 1] = file_name.split("\\")[-1] + "_max"
        
        
    from print_log import print_log        
    for ix in range(len(datas)):
        value = "{:3d} ============================================".format(ix)
        print_log(value, log_file)
        
        data = datas[ix]
        label = labels[ix]
#        data, scale = scale_wave_data(data, label, pre_scale)
#        label = (label*scale).astype(np.int)
        for _i in range(100):
            ok, _, __, start, end, lw = process_data_labels(data, label, debug=True)
            
            if not ok:
                print_log("False, {:5d}, {:5d}, {:3d}, {}".format(
                        start, end, lw, file_index[ix]),
                        log_file)
            
        
if __name__ == "__main__":
    
    path = "../all_data_labels"
    files = [os.path.join(path, item) for item in os.listdir(path)]
    
#    _test_without_scale(files)
    
#    _test_with_scale(files, pre_scale=0.4)
    
    _test_bug(files)
    
    print()
    print("=================================================")
    print("===================Test Over=====================")
    print("=================================================")
    
            
#    import matplotlib.pyplot as plt    
##    plt.figure(figsize=(12, 8))
##    plt.plot(real_data)
##    plt.plot(real_label)
#    
#    data = (data - np.min(data)) / (np.max(data) - np.min(data))
#    label_d = np.zeros_like(data)
#    label = (label*scale).astype(np.int)
#    
#    for x, y in label:
#        label_d[x:y] += 1
#    
#    plt.figure(figsize=(12, 8))
#    plt.plot(data)
#    plt.plot(label_d)
#    plt.show()
    
    
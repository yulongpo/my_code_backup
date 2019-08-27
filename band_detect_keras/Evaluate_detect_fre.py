# -*- coding: utf-8 -*-

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


import time

from band_lib.band_detect import DetectApp, DetectApp_t
from band_lib.waveFileCapture import waveDataScaning
from band_lib.print_log import print_log

import numpy as np

from enum import Enum, unique

@unique
class PhaseMode(Enum):
    TRAIN = 1
    TEST = 2
    VAL = 3
    
TRAIN = PhaseMode.TRAIN
TEST = PhaseMode.TEST
VAL = PhaseMode.VAL


class DataRead(waveDataScaning):
    def __init__(self, mode:PhaseMode=TEST):
        super(DataRead, self).__init__()
        self.mode = mode
        
    def get_data(self, file_name):
        """
        * 取出数据
        
        Parameters
        ----------
        * @file_name: str, 样本名字（路径+名字）
        
        * Returns: [data_ave, data_max]
        ----------
        * @data_ave: list[tuple]，平均谱数据
        * @data_max: list[tuple]，最大谱数据
        """
        self.dataPath = file_name
        self.dataUpdate()
        
        data_ave = []
        data_max = []
        wave_gt_max = []
        wave_gt_ave = []
        
        if self.mode is TRAIN or self.mode is VAL:
            range_num = self.allSigFrame
        if self.mode is TEST:
            range_num = 1
            
        for i in range(range_num):
            self.curSigFrame = i + 1
            self.readCurFrame()
            data_ave.append(self.dataAve)
            data_max.append(self.dataMax)
            _wave_gt_max = []
            _wave_gt_ave = []
            for res in self.waveResult:
                if res.cnr < 5:
                    continue
                if res.midFreq < self.freqStart:
                    continue
                x1 = np.ceil(((res.midFreq - res.bandWidth/2) - 
                              self.freqStart)/self.freqRes).astype(np.int)
                x2 = np.floor(((res.midFreq + res.bandWidth/2) - 
                               self.freqStart)/self.freqRes).astype(np.int)
                if x2 - x1 < 8:
                    continue
                if res.waveFitting == 2:
                    _wave_gt_max.append([x1, x2])
                elif res.waveFitting == 1:
                    _wave_gt_ave.append([x1, x2])
                else:
                    _wave_gt_max.append([x1, x2])
                    _wave_gt_ave.append([x1, x2])
                    
            wave_gt_ave.append(_wave_gt_ave)
            wave_gt_max.append(_wave_gt_max)
                                
        return data_ave, data_max


if __name__ == "__main__":
    data_read = DataRead(VAL)
    
    threshold = 0.5
    
    data_des = 1  # 0: ave, 1: max
    plot = True
    
    data_types = ["Avarage Spectrum", "Maximum Spectrum"]
#    model_path = f"../models/new_best_keras_int_max.h5"
    model_path = "./models/new_best_keras_1.h5"
    
    model_path_name = os.path.splitext(os.path.split(model_path)[-1])[0]
    detection = DetectApp_t(model_path)
    
    data_path = "./data_test"
    files = [os.path.join(data_path, item) for item in os.listdir(data_path)]
    
    print("\n========================================")
    print("==============检测结果==================")
    print("========================================\n")
    
    for i, file in enumerate(files):
        print(i+1, file)
        datas = data_read.get_data(file)
        
        data = datas[data_des][0]
        result = detection.detect(data, shape=False, plot=plot, 
                                  threshold=4.5, data_type=data_types[data_des]+file)

        detection.show()
        if len(result):
            freq_start = data_read.freqStart/1e6
            freq_res = (data_read.freqEnd - data_read.freqStart)/(data_read.fftLen//2)/1e6
            for idx, (x, w, min_v, cnr) in enumerate(result):
                _start = x*freq_res + freq_start
                band_width = w*freq_res
                mid_freq = _start + band_width/2
                amp = min_v + cnr
                
                out_s = f"  {idx+1:3d}: mid_freq={mid_freq:.3f} MHz\tband_width={band_width:.3f} MHz\tCNR={cnr:.3f} dB\tAmptitude={amp:.3f} dB"
                print(out_s)
        print("=============================================\n")
        
#    detection.show()
        
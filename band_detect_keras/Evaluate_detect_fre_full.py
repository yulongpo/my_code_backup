# -*- coding: utf-8 -*-

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import sys

import time

from band_lib.band_detect import DetectApp
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
                                
        return [data_ave, wave_gt_ave], [data_max, wave_gt_max]
    

def calcu_iou(b1, b2):
    """
    b1: [j, 2]
    b2: [2,]
    
    return: [j,]
    
    """
    xmin = np.maximum(b1[:, 0], b2[0])
    xmax = np.minimum(b1[:, 1], b2[1])
    insect_w = np.maximum(xmax - xmin, 0)
    
    b1_w = b1[:, 1] - b1[:, 0]
    b2_w = b2[1] - b2[0]
    
    return insect_w/(b1_w + b2_w - insect_w)

if __name__ == "__main__":
    data_read = DataRead(VAL)
    
    iou_threshold = 0.5
    cnr_threshold = 4
    
    data_des = 1  # 0: ave, 1: max
    plot = False
    logging = not plot
    
    data_type = ["ave", "max"]
    model_path = f"./models/new_best_keras_int_max.h5"
    model_path = f"./models/new_best_keras_1.h5"
    
    model_path_name = os.path.splitext(os.path.split(model_path)[-1])[0]
    detection = DetectApp(model_path)
    
    data_path = "./true_data"
#    data_path = "./new_"
    files = [os.path.join(data_path, item) for item in os.listdir(data_path)]
        
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
    log_file = f"./log/{now}_threshold_{cnr_threshold}_{data_type[data_des]}.txt" if logging else None
    print_log(model_path, log_file, print_flg=False)
    print_log("err_rate - lose_reate\t| index | file_name",
                      log_file, print_flg=False)
    
    all_err_cnt = 0
    all_lose_cnt = 0
    
    all_result = 0
    all_gts = 0
    
    all_ind = 0
    
    for i in range(len(files[:])):
#        i = 60
        print_log(f"{files[i]}:", log_file, print_flg=False)
        datas, gts = data_read.get_data(files[i])[data_des]
        
        _all_ind = 0
        for k in range(len(datas))[:]:
            data = datas[k]
            gt = np.array(gts[k])
           
            result = detection.detect(data, shape=False, plot=plot, threshold=cnr_threshold)
            
            err_cnt = 0
            detect_index_ = []
            for res in result:
                res = np.array(res)
                iou = calcu_iou(gt, res)
            
                if np.max(iou) > iou_threshold:
                    detect_index_.append(np.argmax(iou))
                else:
                    err_cnt += 1
            
            err_rate = err_cnt/len(result)
            detect_index = list(set(detect_index_))
            lose_reate = 1 - len(detect_index)/len(gt)
            print_log(f"err_rate:{err_rate:.3f}({err_cnt}/{len(result)}) - lose_rete:{lose_reate:.3f}({len(gt) - len(detect_index)}/{len(gt)})\t| {i:2d} |",
                      log_file, print_flg=True)
            
            
            all_err_cnt += err_cnt
            all_lose_cnt += len(gt) - len(detect_index)
            all_result += len(result)
            all_gts += len(gt)
            
            _all_ind += len(gt)
            
        all_ind += _all_ind/len(datas)
            
        print_log("\n", log_file, print_flg=False)
       
        
    print_log("\n========================================================\n",
              log_file)
    print_log(f"err_rate:\t{all_err_cnt}/{all_result} = {all_err_cnt/all_result}",
          log_file, print_flg=False)
    print_log(f"lose_rete:\t{all_lose_cnt}/{all_gts} = {all_lose_cnt/all_gts}",
          log_file, print_flg=False)
    
    all_right = all_result - all_err_cnt
    err_rate = all_err_cnt/all_result
    right_rate = 1 - err_rate
    
    all_detected = all_gts - all_lose_cnt
    lose_rate = all_lose_cnt/all_gts
    full_rate = 1 - lose_rate
    
    
    print(f"无重复载波个数：{int(all_ind)}")
    
    print_log("\n========================================================")
    s_right_1 = "载波检准率 = 检出正确载波数/检出载波数"
    s_right_2 = f"检出载波数：{all_result}，检出正确载波数：{all_right}，虚检数：{all_err_cnt}"
    s_right_3 = f"检准率: {all_right}/{all_result} = {100*right_rate:.3f}%\n虚检率: {all_err_cnt}/{all_result} = {100*err_rate:.3f}%"
    
    print(s_right_1)
    print(s_right_2)
    print(s_right_3)
    
    print_log("\n========================================================")
    s_full_1 = "载波检全率 = 检出正确载波数/实际载波数"
    s_full_2 = f"实际载波数：{all_gts}，检出正确载波数：{all_detected}，漏检数：{all_lose_cnt}"
    s_full_3 = f"检全率: {all_detected}/{all_gts} = {100*full_rate:.3f}%\n漏检率: {all_lose_cnt}/{all_gts} = {100*lose_rate:.3f}%"
    
    print(s_full_1)
    print(s_full_2)
    print(s_full_3)
    
    
    
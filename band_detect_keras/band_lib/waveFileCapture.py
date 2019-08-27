# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 14:50:50 2019

@author: huanghao
"""

import numpy as np
from struct import unpack
import os


class waveResult():
    def __init__(self, waveId=None, midFreq=None, amptitude=None, 
                 bandWidth=None, cnr=None, waveFitting=None):
        self.waveId = waveId
        self.midFreq = midFreq
        self.amptitude = amptitude
        self.bandWidth = bandWidth
        self.cnr = cnr
        self.waveFitting = waveFitting
        
class waveDataScaning():
    def __init__(self, dataPath=""):
        
        self.dataPath = dataPath
        self.waveFileName = None #os.path.split(self.dataPath)[-1]
        
        self.isOutPut = None
        self.startDcsLen = 16
        self.outPutHead = b'wavemark 1.0\x00\x00\x00\x00'
        
        self.sigStream = None #open(self.dataPath, "rb")
        self.waveHeadLen = 21

        self.frameHeadLen = 4
        self.frameLabelInfoLen = 8
        self.frameWaveIDLen = 36
        self.frameLabelLen = 24
        self.labelLen = self.frameWaveIDLen + self.frameLabelLen        
        
        self.synCode = None
        self.ver = None
        
        self.sigEndPos = None
        self.curSigFrame = None
        self.allSigFrame = None
        self.framePos = []
        
        self.freqStart = None
        self.freqEnd = None
        self.freqRes = None
        self.specType = None
        self.specBit = None

        self.fftLen = None
        self.dataAve = None
        self.dataMax = None
        
        self.oneResLen = None
        self.waveNums = None
        self.waveResult = []
        
        if self.dataPath:
            self.dataUpdate()
        
    def __del__(self):
        if self.sigStream:
            self.sigStream.close()
            del self.framePos
            del self.waveResult
        
    def dataUpdate(self):
        self.framePos.clear()
        self.waveResult.clear()
        self.waveFileName = os.path.split(self.dataPath)[-1]
        self.sigStream = open(self.dataPath, "rb")
        
        self.sigStream.seek(0, os.SEEK_END)
        self.sigEndPos = self.sigStream.tell()
        self.sigStream.seek(0)
        
        tmpS = unpack("16s", self.sigStream.read(self.startDcsLen))[0]
        if tmpS == self.outPutHead:
            self.isOutPut = True
            self.labelLen = self.frameWaveIDLen + self.frameLabelLen + 1
        else:
            self.isOutPut = False
            self.sigStream.seek(0)
            self.labelLen = self.frameWaveIDLen + self.frameLabelLen
        
#        print(self.isOutPut, "-------------------")
        
        while(self.sigStream.tell() < self.sigEndPos):
            self.framePos.append(self.sigStream.tell())
            self._readCurFrame()
            
        self.allSigFrame = len(self.framePos)
        self.curSigFrame = 1 if self.allSigFrame > 0 else 0
        if self.curSigFrame:
            self.readCurFrame()
        
    def _readCurFrame(self):
        self.synCode = unpack("i", self.sigStream.read(4))
        self.ver = unpack("s", self.sigStream.read(1))
        self.freqStart, self.freqEnd, self.freqRes, self.specType = unpack(
                "2dfs", self.sigStream.read(self.waveHeadLen))
        self.specBit = unpack("i", self.sigStream.read(self.frameHeadLen))

        self.fftLen = unpack("i", self.sigStream.read(self.frameHeadLen))[0]
        self.sigStream.read(int(self.fftLen))
        _, tmpL = unpack("2i", self.sigStream.read(self.frameLabelInfoLen))
        self.sigStream.read(int(tmpL*self.labelLen))

    def readCurFrame(self):
        self.sigStream.seek(self.framePos[self.curSigFrame - 1]) #定位当前帧起点流位置
        
        self.synCode = unpack("i", self.sigStream.read(4))
        self.ver = unpack("s", self.sigStream.read(1))
        self.freqStart, self.freqEnd, self.freqRes, self.specType = unpack(
                "2dfs", self.sigStream.read(self.waveHeadLen))
        self.specBit = unpack("i", self.sigStream.read(self.frameHeadLen))

        self.fftLen = unpack("i", self.sigStream.read(self.frameHeadLen))[0]
        self.dataAve = unpack(str(self.fftLen//2) + "b", self.sigStream.read(self.fftLen//2))
        self.dataMax = unpack(str(self.fftLen//2) + "b", self.sigStream.read(self.fftLen//2))
        self.oneResLen, self.waveNums = unpack("2i", self.sigStream.read(self.frameLabelInfoLen))
        
        self.waveResult.clear()
        for _ in range(self.waveNums):
            tmpRes = waveResult()
            tmpRes.waveId = unpack("36s", self.sigStream.read(self.frameWaveIDLen))
            tmpRes.midFreq, tmpRes.bandWidth, tmpRes.amptitude, tmpRes.cnr = unpack(
                    "2d2f", self.sigStream.read(self.frameLabelLen))
            if self.isOutPut:
                tmpRes.waveFitting = np.frombuffer(self.sigStream.read(1), np.int8)[0]
            else:
                tmpRes.waveFitting = 0
                
            self.waveResult.append(tmpRes)


def getTrainData(wave, waveDataPath, dataType="ave"):
    wave.dataPath = waveDataPath #读入文件路径
    wave.dataUpdate() #更新数据
    
    trainData = []
    valData = []
    
    for index in range(1, wave.allSigFrame + 1):
        wave.curSigFrame = index
        wave.readCurFrame()
        if dataType == "ave":
            trainData.append(np.array(wave.dataAve))
            val = np.zeros(len(wave.dataAve))
            
            for res in wave.waveResult:
                if res.waveFitting == 2:
                    continue
                x1 = np.ceil(((res.midFreq - res.bandWidth/2) - wave.freqStart)/wave.freqRes).astype(np.int)
                x2 = np.floor(((res.midFreq + res.bandWidth/2) - wave.freqStart)/wave.freqRes).astype(np.int)
                
                val[x1 : x2] += 1
            valData.append(val)
                
        elif dataType == "max":
            trainData.append(np.array(wave.dataMax))
            val = np.zeros(len(wave.dataMax))
            
            for res in wave.waveResult:
                if res.waveFitting == 1:
                    continue
                x1 = np.ceil(((res.midFreq - res.bandWidth/2) - wave.freqStart)/wave.freqRes).astype(np.int)
                x2 = np.floor(((res.midFreq + res.bandWidth/2) - wave.freqStart)/wave.freqRes).astype(np.int)
                
                val[x1 : x2] += 1
            valData.append(val)

    trainData = np.array(trainData)
    valData = np.array(valData)

    return trainData, valData
    
    
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    dataPath = r"D:\working\57_signals\waveMark\testPrj\waveMark\output\FFT_2018_08_31_14_838860810_1-3-R-2000_3" #FFT_2018_08_10_11_838860805_Gat10-V-4100_3"
    
#    dataPath = r"D:\working\57_signals\waveMark\testPrj\waveMark\input\FFT_2018_08_10_11_838860805_Gat10-V-4100_3"
    wave = waveDataScaning()
    
#    fig = plt.figure(figsize=(12, 8))
#    ax = fig.add_subplot(111)
#    
#    wave.readCurFrame()
#    freqs = np.linspace(wave.freqStart, wave.freqEnd, wave.fftLen//2)
#
#    ax.plot(freqs, wave.dataAve, "k", label="ave")
#    ax.plot(freqs, wave.dataMax, "b", label="max")
#    
#    ax.set_xlim((wave.freqStart, wave.freqEnd))
#    
#    for res in wave.waveResult:
#        x = res.midFreq - res.bandWidth/2
#        y = res.amptitude - res.cnr
#        w = res.bandWidth
#        h = res.cnr
#        fitting = res.waveFitting
#        
#        if fitting == 2:
#            patch = plt.Rectangle((x, y), w, h, color = "m", alpha = 0.3)
#        elif fitting == 1:
#            patch = plt.Rectangle((x, y), w, h, color = "g", alpha = 0.3)
#        else:
#            patch = plt.Rectangle((x, y), w, h, color = "r", alpha = 0.3)
#        
#        ax.add_patch(patch)
#    
#    plt.show()
#    
#    dataType = "ave"
#    trainData = []
#    valData = []
#    
#    for index in range(1, wave.allSigFrame + 1):
#        wave.curSigFrame = index
#        wave.readCurFrame()
#        labels = []
#        if dataType == "ave":
#            trainData.append(np.array(wave.dataAve))
#            val = np.zeros(len(wave.dataAve))
#            
#            for res in wave.waveResult:
#                if res.waveFitting == 2:
#                    continue
#                x1 = np.ceil(((res.midFreq - res.bandWidth/2) - wave.freqStart)/wave.freqRes).astype(np.int)
#                x2 = np.floor(((res.midFreq + res.bandWidth/2) - wave.freqStart)/wave.freqRes).astype(np.int)
#                
#                val[x1 : x2] += 1
#            valData.append(val)
#                
#        elif dataType == "max":
#            trainData.append(np.array(wave.dataMax))
#            val = np.zeros(len(wave.dataMax))
#            
#            for res in wave.waveResult:
#                if res.waveFitting == 1:
#                    continue
#                x1 = np.ceil(((res.midFreq - res.bandWidth/2) - wave.freqStart)/wave.freqRes).astype(np.int)
#                x2 = np.floor(((res.midFreq + res.bandWidth/2) - wave.freqStart)/wave.freqRes).astype(np.int)
#                
#                val[x1 : x2] += 1
#            valData.append(val)
#            
#    trainData = np.array(trainData)
#    valData = np.array(valData)
    
    trainData, valData = getTrainData(wave, dataPath, "max")
#    ll = list(zip(getTrainData(wave, dataPath, "max")))
    
#    plt.figure(figsize=(12, 8))
#    plt.plot(trainData[0])
#    plt.plot((np.max(trainData[0]) - np.min(trainData[0])) * valData[0] + np.min(trainData[0]))
    
    
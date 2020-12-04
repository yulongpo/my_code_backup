# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 16:24:34 2020

@author: huanghao
"""


# from skimage import io

# im = io.imread("signal_app_24.png")

# print(im.shape)

import numpy as np
import matplotlib.pyplot as plt


def generate_sinusoid(N, A, f0, fs, phi):
    '''
    N(int) : number of samples
    A(float) : amplitude
    f0(float): frequency in Hz
    fs(float): sample rate
    phi(float): initial phase
    
    return 
    x (numpy array): sinusoid signal which lenght is M
    '''
    
    T = 1/fs
    n = np.arange(N)    # [0,1,..., N-1]
    x = A * np.exp(2j*f0*np.pi*n*T + phi)
    # noise_power = 0.001 * fs / 2
    # time = np.arange(N) / fs
    # x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
    
    return x


sig = generate_sinusoid(32768, 1, 200, 1000, 0)

plt.psd(sig, NFFT=1024, Fs=1000, Fc=0)

sig1 = sig*np.exp(2j*(-200)*np.pi*np.arange(len(sig))/1000)
plt.psd(sig1, NFFT=1024, Fs=1000, Fc=0)



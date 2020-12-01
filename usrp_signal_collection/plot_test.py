# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 05:08:15 2020

@author: hh
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

path = "C:/Users/hh/.uhd_ui/usrp_tmp.bin"

with open(path, "rb") as f:
    buff = f.read()
    tmp = np.frombuffer(buff, np.int16)/32768

d_i, d_q = np.reshape(tmp, (-1, 2)).T
data = d_i + 1j*d_q

plt.psd(data[:1024*4], NFFT=1024, Fs=30e6, Fc=100e6)

index = 0
f, ps = signal.welch(data[(index+0)*1024 : (index+8)*1024],
                                      30e6,
                                      signal.windows.blackmanharris(1024),
                                      1024,
                                      scaling='density', return_onesided=False)
plt.figure()
f = f + 100e6
ps = np.fft.fftshift(10*np.log10(np.abs(ps)))

plt.plot(f, ps)
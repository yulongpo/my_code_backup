# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plot_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

# import matplotlib
# matplotlib.use("Qt5Agg")  # 声明使用QT5
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
# from matplotlib.figure import Figure
# import matplotlib.pyplot as plt

import numpy as np
from scipy import signal

# from PyQt5.uic import compileUi, compileUiDir

# with open("plot_window_ui.py", "wt", encoding='utf-8') as pyFile:
#     uiFile = open("plot_window.ui", "r", encoding='utf-8')
#     compileUi(uiFile, pyFile)
#     uiFile.close()

from plot_window_ui import Ui_MainWindow

import pyqtgraph as pg

class PlotWindow(QMainWindow, Ui_MainWindow):
    closed = pyqtSignal()
    def __init__(self):
        super(PlotWindow, self).__init__()
        self.setupUi(self)
        self.resize(1280, 720)
        self.fc = 0.
        self.fs = 0.
        self.sig = np.random.randn(1024*8)
        
        self.index = 0
        self.all_index = len(self.sig)//(1024*8)
        
        self.pw = pg.PlotWidget(name='Plot1', background="k")
        self.pw.showGrid(x=True, y=True)
        self.p1 = self.pw.plot()
        self.p1.setPen((200, 0, 0))
        
        ## Add in some extra graphics
#        rect = QtGui.QGraphicsRectItem(QtCore.QRectF(0, 0, 1, 5e-11))
#        rect.setPen(pg.mkPen(0, 0, 200))
#        self.pw.addItem(rect)
        
        self.pw.setLabel('left', 'PSD', units='dB')
        self.pw.setLabel('bottom', 'Frequncy', units='Hz')
        self.pw.setTitle(title="Power of Density")
        
        
        self.gridLayout.addWidget(self.pw)
##        self.gridLayout.addWidget(self.fig_tool_bar, 0, 1)
#        ## Start a timer to rapidly update the plot in pw
        self.t = QTimer()
        self.t.timeout.connect(self.update_fig)
#        t.start(0.5)
#        self.updateData()
        
#    def rand(self, n):
#        data = np.random.random(n)
#        data[int(n*0.1):int(n*0.13)] += .5
#        data[int(n*0.18)] += 2
#        data[int(n*0.1):int(n*0.13)] *= 5
#        data[int(n*0.18)] *= 20
#        data *= 1e-12
#        return data, np.arange(n, n+len(data)) / float(n)
#    
#
#    def updateData(self):
#        yd, xd = self.rand(10000)
#        print(len(xd))
#        self.p1.setData(y=yd, x=xd)
    

    
#    def update_fig(self, fc=100e6, fs=30e6, sig=np.array([])):
    def update_fig(self):
        self.all_index = len(self.sig) // (1024*32)
        self.index = (self.index + 1) % self.all_index
        
        print("-------------------", self.all_index, self.index)
        _, ps = signal.welch(self.sig[(self.index+0)*1024 : (self.index+32)*1024],
                                      self.fs,
                                      signal.windows.blackmanharris(1024),
                                      1024,
                                      scaling='density', return_onesided=False)
#        f = f + self.fc
#        N = 1024
        f = np.linspace(self.fc-self.fs/2., self.fc+self.fs/2., 1024)
#        ps = np.zeros(N)
#        for ix in range(0, 8):
##            print("ssssssssssssssss", ix, int(ix*N), int((ix+1)*N))
#            fft = np.abs(np.blackman(N)*np.fft.fftshift(
#                    np.fft.fft(self.sig[(self.index+ix)*1024 : (self.index+ix+1)*1024])**2)/N)
#            ps = np.max([ps, fft], axis=0)
        
        
        ps = np.fft.fftshift(10*np.log10(np.abs(ps)))
        print("ssssssssssssssss", np.min(ps), np.max(ps))
        self.pw.setXRange(f[0]-10, f[-1]+10)        
        self.pw.setYRange(np.min(ps)-10, np.max(ps)+10)
        self.p1.setData(y=ps, x=f)
        
    def closeEvent(self, event):
        print(event)
        self.t.stop()
        self.closed.emit()
        
        
        
# class SpectrumFigure(FigureCanvas):
#     def __init__(self):
#         self.fig = Figure()
#         super(SpectrumFigure, self).__init__(self.fig) #此句必不可少，否则不能显示图形
#         self.fig.set_tight_layout(True)
#         self.ax = self.fig.add_subplot(111)
        
#         self.sig = np.random.randn(32768)
#         self.update_fig()
        
#     def update_fig(self):
#         print("-- fig plot --")
#         self.ax.clear()
#         self.ax.psd(self.sig, NFFT=1024, Fc=0, Fs=2200)
#         self.ax.set_xlim((0, 1100))
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = PlotWindow()
    main.show()
    sys.exit(app.exec_())
        
        
        
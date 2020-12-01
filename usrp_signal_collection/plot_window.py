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

import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

from PyQt5.uic import compileUi, compileUiDir

with open("plot_window_ui.py", "wt", encoding='utf-8') as pyFile:
    uiFile = open("plot_window.ui", "r", encoding='utf-8')
    compileUi(uiFile, pyFile)
    uiFile.close()

from plot_window_ui import Ui_MainWindow

class PlotWindow(QMainWindow, Ui_MainWindow):
    closed = pyqtSignal()
    def __init__(self):
        super(PlotWindow, self).__init__()
        self.setupUi(self)
        
        self.plot_fig = SpectrumFigure()
        self.fig_tool_bar = NavigationToolbar(self.plot_fig, None, False)
        self.gridLayout.addWidget(self.plot_fig, 1, 1)
        self.gridLayout.addWidget(self.fig_tool_bar, 0, 1)
        
    def update(self, sig=np.array([])):
        self.plot_fig.sig=sig
        self.plot_fig.update()
        
    def closeEvent(self, event):
        print(event)
        self.closed.emit()
        
        
        
class SpectrumFigure(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        super(SpectrumFigure, self).__init__(self.fig) #此句必不可少，否则不能显示图形
        self.fig.set_tight_layout(True)
        self.ax = self.fig.add_subplot(111)
        
        self.sig = np.random.randn(32768)
        self.update()
        
    def update(self):
        self.ax.psd(self.sig)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = PlotWindow()
    main.show()
    sys.exit(app.exec_())
        
        
        
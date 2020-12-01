# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 21:51:45 2020

@author: hh
"""


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

import os
from os.path import join as pjoin
import numpy as np
import matplotlib.pyplot as plt
import json


from PyQt5.uic import compileUi, compileUiDir

with open("uhd_ui.py", "wt", encoding='utf-8') as pyFile:
    uiFile = open("uhd_ui_2.ui", "r", encoding='utf-8')
    compileUi(uiFile, pyFile)
    uiFile.close()


from uhd_ui import Ui_MainWindow
from plot_window import PlotWindow

import time

import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

class _config():
    gnu_radio_path = r"C:\Program Files\GNURadio-3.7"
    save_path = os.getcwd()
    fc = "100 M"
    fs = "30 M"
    sample_interval = "10 M"
    sample_nums = "100 k"
    sample_times = "1"
    
class Config():
    u2ix_dict = {"":0, "k": 1, "M": 2, "G": 3}
    ix2u_dict = {0: "", 1: "k", 2: "M", 3: "G"}
    gnu_radio_path = ""
    save_path = ""
    fc = 0
    fs = 0
    sample_interval = 0
    sample_nums = 0
    sample_times = 0    
    

class MainWindow(QMainWindow, Ui_MainWindow):
    config_changed = pyqtSignal()
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("USRP B210 信号采样")
        self.setWindowIcon(QIcon("signal_app_24.png"))
                
        self.plot_win = PlotWindow()
        
        # qss = "QWidget#MainWindow{background-color:red;}"
        # qss = "QWidget#MainWindow{border-image:url(signal_app_24.png);}"
        # self.setStyleSheet(qss)
        
        self.home_dir = pjoin(os.path.expanduser("~"), ".uhd_ui")
        self.config_path = pjoin(self.home_dir, "config.json")
        # self.tmp_sample_file = pjoin(self.home_dir, "usrp_tmp.bin")
        
        self.CONFIG = {}
        self.config = Config()
        
        self.view_spec_config = Config()
        self.view_spec_config.save_path = self.home_dir
        self.view_spec_config.sample_times = 1
        self.view_spec_config.sample_nums = 1*1024*1024
        
        self.sample_thread = SampleThread()
        
        self.initial()
        
#
        self.save_path_btn.clicked.connect(self.open_folder)
        self.gnu_radio_btn.clicked.connect(self.open_gnu_folder)
        
        self.ok_btn.clicked.connect(self.sample_thread_start)
        self.ok_btn.setToolTip("开始采集信号")
        
        self.plot_btn.clicked.connect(self.plot_psd_start)
        self.plot_win.closed.connect(self.plot_psd_stop)
        
        self.stop_btn.setEnabled(False)
        self.stop_btn.setToolTip("停止当前信号采样")
        self.stop_btn.clicked.connect(self.stop_current_sampling)
        
        self.advance_groupBox.hide()
        self.advance_mode = False
        self.advance_mode_btn.setText("打开高级模式")
        self.advance_mode_btn.clicked.connect(self.set_advance_mode)
        
        self.sample_thread.one_sample_end[int, str].connect(self.one_sample_end)
        self.sample_thread.all_sample_end.connect(self.sample_thread_end)
        self.sample_thread.spec_data_get[int, int, list].connect(self.plot_psd)
#        
        
        self.gnu_radio_path_edit.textChanged[str].connect(self.new_gnu_radio_path)
        self.save_path_edit.textChanged[str].connect(self.new_save_path)
        self.fc_spinBox.valueChanged[int].connect(self.new_fc_val)
        self.fc_comboBox.currentIndexChanged[int].connect(self.new_fc_cbox)
        self.fs_spinBox.valueChanged[int].connect(self.new_fs_val)
        self.fs_comboBox.currentIndexChanged[int].connect(self.new_fs_cbox)
        self.sample_interval_spinBox.valueChanged[int].connect(self.new_sample_interval_val)
        self.sample_interval_comboBox.currentIndexChanged[int].connect(self.new_sample_interval_cbox)
        self.sample_nums_spinBox.valueChanged[int].connect(self.new_n_sample_val)
        self.sample_nums_comboBox.currentIndexChanged[int].connect(self.new_n_sample_cbox)
        self.sample_times_spinBox.valueChanged[int].connect(self.new_sample_times)
        
        self.config_changed.connect(self.update_config)
    # @pyqtSignal(int, int)
    # def resizeEvent(self, event):
    #     v_size = int(self.height()/36)        
    #     QMainWindow.resizeEvent(self, event)
        
    def closeEvent(self, event):
        self.plot_win.close()
        self.sample_thread.terminate()
        self.sample_thread.wait()
        
        
    def initial(self):
        def _get(s_cfg, index=0):
            s_cfg = s_cfg.split()
            if len(s_cfg) == 2:
                try:
                    index = self.config.u2ix_dict[s_cfg[1]]
                    return s_cfg[0], index
                except:
                    raise ValueError("配置出错！")
            elif len(s_cfg) == 1:
                return s_cfg[0], index
            else:
                raise ValueError("配置出错！")
                
        if not os.path.exists(self.home_dir):
            os.makedirs(self.home_dir)
        if not os.path.exists(self.config_path):
            initial_config = _config()
            self.CONFIG["gnu_radio_path"] = initial_config.gnu_radio_path
            self.CONFIG["save_path"] = initial_config.save_path
            self.CONFIG["FC"] = initial_config.fc
            self.CONFIG["FS"] = initial_config.fs
            self.CONFIG["sample_interval"] = initial_config.sample_interval
            self.CONFIG["sample_nums"] = initial_config.sample_nums
            self.CONFIG["sample_times"] = initial_config.sample_times
            self.save_config()
            
            self.gnu_radio_path_edit.setText(self.CONFIG["gnu_radio_path"])
            self.save_path_edit.setText(self.CONFIG["save_path"])
            
            _fc, _fc_index = _get(self.CONFIG["FC"])
            self.fc_spinBox.setValue(int(_fc))
            self.fc_comboBox.setCurrentIndex(_fc_index)
            
            _fs, _fs_index = _get(self.CONFIG["FS"])
            self.fs_spinBox.setValue(int(_fs))
            self.fs_comboBox.setCurrentIndex(_fs_index)
            
            _interval, _interval_index = _get(self.CONFIG["sample_interval"])
            self.sample_interval_spinBox.setValue(int(_interval))
            self.sample_interval_comboBox.setCurrentIndex(_interval_index)
            
            _n_sample, _n_index = _get(self.CONFIG["sample_nums"])
            self.sample_nums_spinBox.setValue(int(_n_sample))
            self.sample_nums_comboBox.setCurrentIndex(_n_index)
            
            self.sample_times_spinBox.setValue(int(self.CONFIG["sample_times"]))
        else:
            with open(self.config_path, "r") as f:
                self.CONFIG = json.load(f)
                self.config_changed.emit()
                
                self.gnu_radio_path_edit.setText(self.CONFIG["gnu_radio_path"])
                self.save_path_edit.setText(self.CONFIG["save_path"])
                
                _fc, _fc_index = _get(self.CONFIG["FC"])
                self.fc_spinBox.setValue(int(_fc))
                self.fc_comboBox.setCurrentIndex(_fc_index)
                
                _fs, _fs_index = _get(self.CONFIG["FS"])
                self.fs_spinBox.setValue(int(_fs))
                self.fs_comboBox.setCurrentIndex(_fs_index)
                
                _interval, _interval_index = _get(self.CONFIG["sample_interval"])
                self.sample_interval_spinBox.setValue(int(_interval))
                self.sample_interval_comboBox.setCurrentIndex(_interval_index)
            
                _n_sample, _n_index = _get(self.CONFIG["sample_nums"])
                self.sample_nums_spinBox.setValue(int(_n_sample))
                self.sample_nums_comboBox.setCurrentIndex(_n_index)
                
                self.sample_times_spinBox.setValue(int(self.CONFIG["sample_times"]))
                
        self.update_config()
        
        
    def save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.CONFIG, f)
        self.config_changed.emit()
        
    def update_config(self):
        def get_value(cfg, u=1000):
            val, unit = cfg.split() if len(cfg.split()) > 1 else [cfg.split()[0], ""]
            val = int(int(val) * u**self.config.u2ix_dict[unit])
            return val
        
        self.config.gnu_radio_path = self.CONFIG["gnu_radio_path"]
        self.config.save_path = self.CONFIG["save_path"]
        
        self.config.fc = get_value(self.CONFIG["FC"])
        self.config.fs = get_value(self.CONFIG["FS"])
        self.config.sample_interval = get_value(self.CONFIG["sample_interval"])
        self.config.sample_nums = get_value(self.CONFIG["sample_nums"], 1024)
        self.config.sample_times = int(self.CONFIG["sample_times"])
        
        self.view_spec_config.gnu_radio_path = self.config.gnu_radio_path
        self.view_spec_config.fc = self.config.fc
        self.view_spec_config.fs = self.config.fs
        
        print(f"---- config changed ----\n\
    GNU Radio 安装目录:\t{self.config.gnu_radio_path} \n\
    文件保存路径:\t{self.config.save_path} \n\
    中心频率:\t\t{self.config.fc} \n\
    采样带宽:\t\t{self.config.fs} \n\
    采样间隔:\t\t{self.config.sample_interval} \n\
    采样点数:\t\t{self.config.sample_nums} \n\
    采样次数:\t\t{self.config.sample_times} \n")
    
        
    def sample_thread_start(self):
        self.textEdit.append("---- 开始采样 ----\n")
        self.sample_thread.config = self.config
        self.sample_thread.mode = 2  # test_mode
        self.sample_thread.start_sample = True
        self.sample_thread.start()
        
        self.plot_btn.setEnabled(False)
        self.plot_btn.setToolTip("正在采集信号, 无法查看当前频谱")
        self.stop_btn.setEnabled(True)
        
        self.ok_btn.setEnabled(False)

    def one_sample_end(self, ix, output_path):
        self.textEdit.append(f"第 {ix} 次采样完成，共 {self.config.sample_times} 次，文件保存路径：{output_path}")
        
    def sample_thread_end(self):
        self.textEdit.append("\n---- 采样结束 ----")
        self.ok_btn.setEnabled(True)
        self.plot_btn.setEnabled(True)
        self.plot_btn.setToolTip("查看当前频谱")
        self.stop_btn.setEnabled(False)
        
    def stop_current_sampling(self):
        self.textEdit.append("---- 停止采样 ----\n")
        self.stop_btn.setEnabled(False)
        self.sample_thread.terminate()
        self.sample_thread.wait()
        
        self.plot_btn.setEnabled(True)
        self.plot_btn.setToolTip("查看当前频谱")
        
    def plot_psd_start(self):
        self.textEdit.append("---- 查看频谱 ----\n")
        self.sample_thread.out_file_name = "usrp_tmp.bin"
        self.sample_thread.config = self.view_spec_config
        
        self.sample_thread.mode = 0
        self.sample_thread.start_sample = True
        
        self.sample_thread.start()
        
        self.ok_btn.setEnabled(False)
        
        
    @pyqtSlot(int, int, list)
    def plot_psd(self, fc, fs, data):
        print("-- plot --")
        self.plot_win.show()
        print(fc, fs)
        self.plot_win.fc = self.config.fc
        self.plot_win.fs = self.config.fs
        self.plot_win.sig = data
        self.plot_win.t.start(50)
#        self.plot_win.update_fig(fc, fs, data)
        
    def plot_psd_stop(self):
        self.sample_thread.terminate()
        self.sample_thread.wait()
        self.ok_btn.setEnabled(True)
        
    def set_advance_mode(self):
        self.advance_mode = not self.advance_mode
        if self.advance_mode:
            self.advance_groupBox.show()
            self.advance_mode_btn.setText("退出高级模式")
        else:
            self.advance_groupBox.hide()
            self.advance_mode_btn.setText("打开高级模式")
        
#    def work_start(self):
#        self.fc = int(100*1e6) #self.start_step * self.delta_f
#        self.bw = self.fs
##        self.n_sample = 1000#int(400*1024*1024)
#        self.out_file_name = "{}/{}_fc_{:d}_bw_{:d}_N_{:d}.dat".format(self.save_dir,
#                              self.get_time(),
#                              self.fc, self.bw, self.n_sample)
#        self.args = ["D:\\mySoftWare\\gnu_radio\\bin\\run_gr.bat",
#                   "D:\\mySoftWare\\gnu_radio\\bin\\uhd_rx_cfile.py"]
#        self.args.append(self.out_file_name)
#        self.args.append("-s")
#        self.args.append("-f {:d}".format(self.fc))
#        self.args.append("-r {:d}".format(self.bw))
#        self.args.append("-N {:d}".format(self.n_sample))
#        
#        print(self.start_step, self.out_file_name)
#        
#        self.process.start("powershell", self.args)
#        self.process.waitForStarted()
#        self.process.waitForFinished()
#        self.process.exitCode()
#        self.textEdit.append("OK! - {}\n==========================\n".format(self.out_file_name))
#
#        
#    
#    def update_args(self):
#        self.fc = int(self.fc_spinBox.value())*(1000**(2 - self.comboBox.currentIndex()))
#        self.bw = int(self.bw_spinBox.value())*(1000**(2 - self.comboBox_2.currentIndex()))
#        self.n_sample = int(self.sample_nums_doubleSpinBox.value())
#        
#        self.out_file_name = "{}/{}_FFT_fc_{}_bw_{}_N_{}.dat".format(self.save_dir,
#                              self.get_time(),
#                              self.fc, self.bw, self.n_sample)
#        self.args = ["D:\\mySoftWare\\gnu_radio\\bin\\run_gr.bat",
#                   "D:\\mySoftWare\\gnu_radio\\bin\\uhd_rx_cfile.py"]
#        self.args.append(self.out_file_name)
#        self.args.append("-s")
#        self.args.append("-f {}".format(self.fc))
#        self.args.append("-r {}".format(self.bw))
#        self.args.append("-N {}".format(self.n_sample))
#        
#        print(self.fc, self.bw, self.n_sample)
#        print(self.out_file_name)
#        
#        
#    def get_time(self):
#        now = int(time.time())     # 1533952277
#        timeArray = time.localtime(now)
#        strTime = time.strftime("%Y-%m-%d-%H-%M-%S", timeArray)
#        
#        return strTime
#
    def open_folder(self):
        dataPath = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                             "选择文件保存路径",
                                                             self.CONFIG["save_path"],
                                                             QtWidgets.QFileDialog.ShowDirsOnly)
        if dataPath == "":
            return
        else:
            self.save_path_edit.setText(dataPath)
    
    def open_gnu_folder(self):
        dataPath = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                             "打开GNU Radio/bin目录",
                                                             self.CONFIG["gnu_radio_path"],
                                                             QtWidgets.QFileDialog.ShowDirsOnly)
        if dataPath == "":
            return
        else:
            self.gnu_radio_path_edit.setText(dataPath)

                
    @pyqtSlot(str)
    def new_gnu_radio_path(self, path):
        self.textEdit.append("gnu_path_changed: " + path)
        self.CONFIG["gnu_radio_path"] = path
        self.save_config()
    
    @pyqtSlot(str)
    def new_save_path(self, path):
        self.textEdit.append("save_path_changed: " + path)
        self.CONFIG["save_path"] = path
        self.save_config()
    
    @pyqtSlot(int)
    def new_fc_val(self, val):
        unit = self.config.ix2u_dict[self.fc_comboBox.currentIndex()]
        new_fc = f"{int(val)} {unit}"
        self.textEdit.append("FC: " + new_fc + "Hz")
        self.CONFIG["FC"] = new_fc
        self.save_config()
        
    @pyqtSlot(int)
    def new_fc_cbox(self, ix):
        try:
            unit = self.config.ix2u_dict[ix]
        except KeyError:
            raise ValueError("设置出错")
        new_fc = f"{self.fc_spinBox.value()} {unit}"
        self.textEdit.append("FC: " + new_fc + "Hz")
        self.CONFIG["FC"] = new_fc
        self.save_config()
        
    @pyqtSlot(int)
    def new_fs_val(self, val):
        unit = self.config.ix2u_dict[self.fs_comboBox.currentIndex()]
        new_fs = f"{int(val)} {unit}"
        self.textEdit.append("FS: " + new_fs + "Hz")
        self.CONFIG["FS"] = new_fs
        self.save_config()
        
    @pyqtSlot(int)
    def new_fs_cbox(self, ix):
        try:
            unit = self.config.ix2u_dict[ix]
        except KeyError:
            raise ValueError("设置出错")
        new_fs = f"{self.fs_spinBox.value()} {unit}"
        self.textEdit.append("FS: " + new_fs + "Hz")
        self.CONFIG["FS"] = new_fs
        self.save_config()
        
    @pyqtSlot(int)
    def new_sample_interval_val(self, val):
        unit = self.config.ix2u_dict[self.sample_interval_comboBox.currentIndex()]
        new_sample_interval = f"{int(val)} {unit}"
        self.textEdit.append("sample_interval: " + new_sample_interval + "Hz")
        self.CONFIG["sample_interval"] = new_sample_interval
        self.save_config()
        
    @pyqtSlot(int)
    def new_sample_interval_cbox(self, ix):
        try:
            unit = self.config.ix2u_dict[ix]
        except KeyError:
            raise ValueError("设置出错")
        new_sample_interval = f"{self.sample_interval_spinBox.value()} {unit}"
        self.textEdit.append("sample_interval: " + new_sample_interval + "Hz")
        self.CONFIG["sample_interval"] = new_sample_interval
        self.save_config()
        
    @pyqtSlot(int)
    def new_n_sample_val(self, val):
        unit = self.config.ix2u_dict[self.sample_nums_comboBox.currentIndex()]
        new_n_sample = f"{int(val)} {unit}"
        # new_n_sample = f"{int(val)} {_d[self.sample_nums_comboBox.currentIndex()]}"
        self.textEdit.append("sample_num: " + new_n_sample)
        self.CONFIG["sample_nums"] = new_n_sample
        self.save_config()
        
    @pyqtSlot(int)
    def new_n_sample_cbox(self, ix):
        try:
            unit = self.config.ix2u_dict[ix]
        except KeyError:
            raise ValueError("设置出错")
        new_n_sample = f"{self.sample_nums_spinBox.value()} {unit}"
        self.textEdit.append("sample_num: " + new_n_sample)
        self.CONFIG["sample_nums"] = new_n_sample
        self.save_config()
        
    @pyqtSlot(int)
    def new_sample_times(self, val):
        new_times = str(val)
        self.textEdit.append("sample_times: " + new_times)
        self.CONFIG["sample_times"] = new_times
        self.save_config()
        
#                
#    def plot_save_sig(self):
#        if self.out_file_name is None:
#            self.textEdit.append("没有采集信号！\n")
#            return
#        if not os.path.isfile(self.out_file_name):
#            self.textEdit.append(self.out_file_name + " 没有保存")
#            return
#        
#        with open(self.out_file_name, "rb") as f:
#            f.seek(0, os.SEEK_END)
#            if f.tell() < 1024*4:
#                buff = f.read()
#            else:
#                buff = f.read(1024*4)
#            data = np.frombuffer(buff, np.int16)
#        
#        d_i, d_q = np.reshape(data, (-1, 2)).T
#
#        spec = np.fft.fft(d_i + 1j*d_q, 1024)
#        
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
    x = A * np.sin( 2*f0*np.pi*n*T + phi )
    noise_power = 0.001 * fs / 2
    time = np.arange(N) / fs
    x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
    
    return x

class SampleThread(QThread):
    one_sample_end = pyqtSignal(int, str)
    all_sample_end = pyqtSignal()
    tmp_sample_end = pyqtSignal()
    spec_data_get = pyqtSignal(int, int, list)
    
    def __init__(self):
        super(SampleThread, self).__init__()
        self.out_file_name = ""
        self.config = Config()
        self.start_sample = False
        self.mode = 0  # 0: psd  1: sample
        
    def __del__(self):
        self.start_sample = False
        self.wait()
        
    
    def view_psd_mode(self):
        bat = pjoin(self.config.gnu_radio_path, "run_gr.bat")
        rx_py = pjoin(self.config.gnu_radio_path, "uhd_rx_cfile.py")
        output_path = pjoin(self.config.save_path, self.out_file_name)
        
        print(f"{bat} {rx_py} {output_path} -s -f {self.config.fc} -r {self.config.fs} -N {self.config.sample_nums}")
        
        print("查看频谱模式")
        while True:
            os.spawnl(os.P_WAIT, bat, f"{bat} {rx_py} {output_path} -s -f {self.config.fc} -r {self.config.fs} -N {self.config.sample_nums}")
            with open(output_path, "rb") as f:
                buff = f.read()
                tmp = np.frombuffer(buff, np.int16)/32768
            
            d_i, d_q = np.reshape(tmp, (-1, 2)).T
            data = d_i + 1j*d_q
#            time.sleep(5)
            self.spec_data_get.emit(self.config.fc, self.config.fs, list(data))
            print("++++++++++++++++++++++++++++++++++++++++++++++")
            print(self.config.fc, self.config.fs)
            print("++++++++++++++++++++++++++++++++++++++++++++++")
#            self.spec_data_get.emit(self.config.fc, self.config.fs, list(data))
#            time.sleep(0.1)
    
    def sample_mode(self):
        print("采样模式")
        pass
    
    def test_mode(self):
        print("测试模式")
        if not os.path.exists("./data_sampled"):
            os.makedirs("./data_sampled")
            
        for i in range(self.config.sample_times):
            os.spawnl(os.P_WAIT, "D:\\program\\GNURadio-3.7\\bin\\run_gr.bat",
                      f"D:\\program\\GNURadio-3.7\\bin\\run_gr.bat \
                          D:\\program\\GNURadio-3.7\\bin\\uhd_rx_cfile.py ./data_sampled/test_{i+1}.bin \
                              -s -f 100000000 -r 1000000 -N 1024")
            self.one_sample_end.emit(i+1, os.path.abspath(f"./data_sampled/test_{i+1}.bin"))
        self.all_sample_end.emit()
        
    def run(self):
        while self.start_sample:
            if self.mode == 0:
                self.view_psd_mode()
            elif self.mode == 1:
                self.sample_mode()
            elif self.mode == 2:
                self.test_mode()
            else:
                raise ValueError(f"采样线程模式设置错误：{self.mode}")
            print('wwwwwwwwwwwwwwwwwwwwwwwwwww')
            self.start_sample = False
            
            
                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uhd_ui_2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 720)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1080, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("signal_app_24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setMinimumSize(QtCore.QSize(120, 0))
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.gnu_radio_path_edit = QtWidgets.QLineEdit(self.groupBox)
        self.gnu_radio_path_edit.setObjectName("gnu_radio_path_edit")
        self.horizontalLayout_6.addWidget(self.gnu_radio_path_edit)
        self.gnu_radio_btn = QtWidgets.QPushButton(self.groupBox)
        self.gnu_radio_btn.setMinimumSize(QtCore.QSize(80, 0))
        self.gnu_radio_btn.setObjectName("gnu_radio_btn")
        self.horizontalLayout_6.addWidget(self.gnu_radio_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setMinimumSize(QtCore.QSize(120, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.save_path_edit = QtWidgets.QLineEdit(self.groupBox)
        self.save_path_edit.setObjectName("save_path_edit")
        self.horizontalLayout_2.addWidget(self.save_path_edit)
        self.save_path_btn = QtWidgets.QPushButton(self.groupBox)
        self.save_path_btn.setMinimumSize(QtCore.QSize(80, 0))
        self.save_path_btn.setObjectName("save_path_btn")
        self.horizontalLayout_2.addWidget(self.save_path_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.fc_label = QtWidgets.QLabel(self.groupBox)
        self.fc_label.setMinimumSize(QtCore.QSize(120, 0))
        self.fc_label.setObjectName("fc_label")
        self.horizontalLayout_3.addWidget(self.fc_label)
        self.fc_spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.fc_spinBox.setMinimumSize(QtCore.QSize(200, 0))
        self.fc_spinBox.setMinimum(1)
        self.fc_spinBox.setMaximum(600000000)
        self.fc_spinBox.setProperty("value", 100)
        self.fc_spinBox.setObjectName("fc_spinBox")
        self.horizontalLayout_3.addWidget(self.fc_spinBox)
        self.fc_comboBox = QtWidgets.QComboBox(self.groupBox)
        self.fc_comboBox.setMinimumSize(QtCore.QSize(120, 0))
        self.fc_comboBox.setMaxCount(4)
        self.fc_comboBox.setObjectName("fc_comboBox")
        self.fc_comboBox.addItem("")
        self.fc_comboBox.addItem("")
        self.fc_comboBox.addItem("")
        self.fc_comboBox.addItem("")
        self.horizontalLayout_3.addWidget(self.fc_comboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setMinimumSize(QtCore.QSize(120, 0))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.fs_spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.fs_spinBox.setMinimumSize(QtCore.QSize(200, 0))
        self.fs_spinBox.setMinimum(1)
        self.fs_spinBox.setMaximum(999999999)
        self.fs_spinBox.setProperty("value", 20)
        self.fs_spinBox.setObjectName("fs_spinBox")
        self.horizontalLayout_4.addWidget(self.fs_spinBox)
        self.fs_comboBox = QtWidgets.QComboBox(self.groupBox)
        self.fs_comboBox.setMinimumSize(QtCore.QSize(120, 0))
        self.fs_comboBox.setMaxCount(3)
        self.fs_comboBox.setObjectName("fs_comboBox")
        self.fs_comboBox.addItem("")
        self.fs_comboBox.addItem("")
        self.fs_comboBox.addItem("")
        self.horizontalLayout_4.addWidget(self.fs_comboBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_4)
        self.gridLayout_2.addLayout(self.horizontalLayout_9, 2, 0, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setMinimumSize(QtCore.QSize(120, 0))
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_8.addWidget(self.label_8)
        self.sample_nums_spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.sample_nums_spinBox.setMinimumSize(QtCore.QSize(200, 0))
        self.sample_nums_spinBox.setMinimum(1)
        self.sample_nums_spinBox.setMaximum(999999999)
        self.sample_nums_spinBox.setObjectName("sample_nums_spinBox")
        self.horizontalLayout_8.addWidget(self.sample_nums_spinBox)
        self.sample_nums_comboBox = QtWidgets.QComboBox(self.groupBox)
        self.sample_nums_comboBox.setMinimumSize(QtCore.QSize(120, 0))
        self.sample_nums_comboBox.setMaxCount(3)
        self.sample_nums_comboBox.setObjectName("sample_nums_comboBox")
        self.sample_nums_comboBox.addItem("")
        self.sample_nums_comboBox.addItem("")
        self.sample_nums_comboBox.addItem("")
        self.horizontalLayout_8.addWidget(self.sample_nums_comboBox)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.horizontalLayout_11.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setMinimumSize(QtCore.QSize(120, 0))
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_7.addWidget(self.label_7)
        self.sample_times_spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.sample_times_spinBox.setMinimumSize(QtCore.QSize(200, 0))
        self.sample_times_spinBox.setMinimum(1)
        self.sample_times_spinBox.setMaximum(999999999)
        self.sample_times_spinBox.setObjectName("sample_times_spinBox")
        self.horizontalLayout_7.addWidget(self.sample_times_spinBox)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.advance_mode_btn = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.advance_mode_btn.sizePolicy().hasHeightForWidth())
        self.advance_mode_btn.setSizePolicy(sizePolicy)
        self.advance_mode_btn.setMaximumSize(QtCore.QSize(80, 16777215))
        self.advance_mode_btn.setObjectName("advance_mode_btn")
        self.horizontalLayout_7.addWidget(self.advance_mode_btn)
        self.horizontalLayout_11.addLayout(self.horizontalLayout_7)
        self.gridLayout_2.addLayout(self.horizontalLayout_11, 3, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.advance_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.advance_groupBox.setTitle("")
        self.advance_groupBox.setObjectName("advance_groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.advance_groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.advance_groupBox)
        self.label_5.setMinimumSize(QtCore.QSize(120, 0))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.sample_interval_spinBox = QtWidgets.QSpinBox(self.advance_groupBox)
        self.sample_interval_spinBox.setMinimumSize(QtCore.QSize(200, 0))
        self.sample_interval_spinBox.setMinimum(0)
        self.sample_interval_spinBox.setMaximum(999999999)
        self.sample_interval_spinBox.setProperty("value", 0)
        self.sample_interval_spinBox.setObjectName("sample_interval_spinBox")
        self.horizontalLayout_5.addWidget(self.sample_interval_spinBox)
        self.sample_interval_comboBox = QtWidgets.QComboBox(self.advance_groupBox)
        self.sample_interval_comboBox.setMinimumSize(QtCore.QSize(120, 0))
        self.sample_interval_comboBox.setMaxCount(3)
        self.sample_interval_comboBox.setObjectName("sample_interval_comboBox")
        self.sample_interval_comboBox.addItem("")
        self.sample_interval_comboBox.addItem("")
        self.sample_interval_comboBox.addItem("")
        self.horizontalLayout_5.addWidget(self.sample_interval_comboBox)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.stop_fc_label = QtWidgets.QLabel(self.advance_groupBox)
        self.stop_fc_label.setMinimumSize(QtCore.QSize(120, 0))
        self.stop_fc_label.setObjectName("stop_fc_label")
        self.horizontalLayout_5.addWidget(self.stop_fc_label)
        self.stop_fc_spinBox = QtWidgets.QSpinBox(self.advance_groupBox)
        self.stop_fc_spinBox.setMinimumSize(QtCore.QSize(200, 0))
        self.stop_fc_spinBox.setMaximum(999999999)
        self.stop_fc_spinBox.setObjectName("stop_fc_spinBox")
        self.horizontalLayout_5.addWidget(self.stop_fc_spinBox)
        self.stop_fc_comboBox = QtWidgets.QComboBox(self.advance_groupBox)
        self.stop_fc_comboBox.setMinimumSize(QtCore.QSize(120, 0))
        self.stop_fc_comboBox.setObjectName("stop_fc_comboBox")
        self.stop_fc_comboBox.addItem("")
        self.stop_fc_comboBox.addItem("")
        self.stop_fc_comboBox.addItem("")
        self.stop_fc_comboBox.addItem("")
        self.horizontalLayout_5.addWidget(self.stop_fc_comboBox)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.advance_groupBox, 1, 0, 1, 1)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem6)
        self.gridLayout_3.addLayout(self.horizontalLayout_12, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.plot_btn = QtWidgets.QPushButton(self.centralwidget)
        self.plot_btn.setMinimumSize(QtCore.QSize(150, 50))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(18)
        self.plot_btn.setFont(font)
        self.plot_btn.setObjectName("plot_btn")
        self.horizontalLayout.addWidget(self.plot_btn)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem8)
        self.ok_btn = QtWidgets.QPushButton(self.centralwidget)
        self.ok_btn.setMinimumSize(QtCore.QSize(150, 50))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.ok_btn.setFont(font)
        self.ok_btn.setObjectName("ok_btn")
        self.horizontalLayout.addWidget(self.ok_btn)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem9)
        self.stop_btn = QtWidgets.QPushButton(self.centralwidget)
        self.stop_btn.setMinimumSize(QtCore.QSize(150, 50))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(18)
        self.stop_btn.setFont(font)
        self.stop_btn.setObjectName("stop_btn")
        self.horizontalLayout.addWidget(self.stop_btn)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem10)
        self.gridLayout_3.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 4, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet("")
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_3.addWidget(self.textEdit, 5, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.fc_comboBox.setCurrentIndex(2)
        self.fs_comboBox.setCurrentIndex(2)
        self.sample_nums_comboBox.setCurrentIndex(2)
        self.sample_interval_comboBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "USRP B210 信号采样"))
        self.label_6.setText(_translate("MainWindow", "GNU Radio 安装目录："))
        self.gnu_radio_btn.setText(_translate("MainWindow", "选择"))
        self.label_2.setText(_translate("MainWindow", "文件保存路径："))
        self.save_path_btn.setText(_translate("MainWindow", "选择"))
        self.fc_label.setText(_translate("MainWindow", "中心频率："))
        self.fc_comboBox.setItemText(0, _translate("MainWindow", "Hz"))
        self.fc_comboBox.setItemText(1, _translate("MainWindow", "kHz"))
        self.fc_comboBox.setItemText(2, _translate("MainWindow", "MHz"))
        self.fc_comboBox.setItemText(3, _translate("MainWindow", "GHz"))
        self.label_4.setText(_translate("MainWindow", "采样带宽："))
        self.fs_comboBox.setItemText(0, _translate("MainWindow", "Hz"))
        self.fs_comboBox.setItemText(1, _translate("MainWindow", "kHz"))
        self.fs_comboBox.setItemText(2, _translate("MainWindow", "MHz"))
        self.label_8.setText(_translate("MainWindow", "样点个数："))
        self.sample_nums_comboBox.setItemText(0, _translate("MainWindow", "    (*1)"))
        self.sample_nums_comboBox.setItemText(1, _translate("MainWindow", "k  (*1024)"))
        self.sample_nums_comboBox.setItemText(2, _translate("MainWindow", "M (*1024*1024)"))
        self.label_7.setText(_translate("MainWindow", "采集次数："))
        self.advance_mode_btn.setText(_translate("MainWindow", "退出高级模式"))
        self.label_5.setText(_translate("MainWindow", "采样间隔："))
        self.sample_interval_comboBox.setItemText(0, _translate("MainWindow", "Hz"))
        self.sample_interval_comboBox.setItemText(1, _translate("MainWindow", "kHz"))
        self.sample_interval_comboBox.setItemText(2, _translate("MainWindow", "MHz"))
        self.stop_fc_label.setText(_translate("MainWindow", "结束中频："))
        self.stop_fc_comboBox.setItemText(0, _translate("MainWindow", "Hz"))
        self.stop_fc_comboBox.setItemText(1, _translate("MainWindow", "kHz"))
        self.stop_fc_comboBox.setItemText(2, _translate("MainWindow", "MHz"))
        self.stop_fc_comboBox.setItemText(3, _translate("MainWindow", "GHz"))
        self.plot_btn.setText(_translate("MainWindow", "查看频谱"))
        self.ok_btn.setText(_translate("MainWindow", "开始采样"))
        self.stop_btn.setText(_translate("MainWindow", "停止采样"))
        self.label.setText(_translate("MainWindow", "当前状态："))


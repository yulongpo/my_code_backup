# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 15:38:31 2020

@author: huanghao
"""


import subprocess
import os

# "D:\\mySoftWare\\gnu_radio\\bin\\run_gr.bat",
#                   "D:\\mySoftWare\\gnu_radio\\bin\\uhd_rx_cfile.py"

# "G:/Program Files/GNURadio-3.7\\bin\\run_gr.bat G:/Program Files/GNURadio-3.7\\bin\\uhd_rx_cfile.py"
path = os.path.abspath(os.curdir)
print(path)
for i in range(2):
    proc = subprocess.Popen(f"D:\\program\\GNURadio-3.7\\bin\\run_gr.bat D:\\program\\GNURadio-3.7\\bin\\uhd_rx_cfile.py data_sampled/test_{i+1}.bin -s -f 100000000 -r 1000000 -N 2048", stdin=subprocess.PIPE, cwd=path)
    proc.wait()
    # proc.stdin("--help")
proc.stdin.close()

print("============================")
print(proc.returncode)

for i in range(2, 4):
    os.spawnl(os.P_WAIT, "D:\\program\\GNURadio-3.7\\bin\\run_gr.bat", f"D:\\program\\GNURadio-3.7\\bin\\run_gr.bat D:\\program\\GNURadio-3.7\\bin\\uhd_rx_cfile.py data_sampled/test_{i+1}.bin -s -f 100000000 -r 1000000 -N 1024")

print("+++++++++++++++++++++++")
# a = input()


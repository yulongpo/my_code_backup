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
for i in range(10):
    proc = subprocess.Popen(f"C:/GNURadio-3.7\\bin\\run_gr.bat C:/GNURadio-3.7\\bin\\uhd_rx_cfile.py test_{i+1}.bin -s -f 100000000 -r 1000000 -N 1048576", stdin=subprocess.PIPE, cwd=path)
    proc.wait()
    # proc.stdin("--help")
proc.stdin.close()

print("============================")
print(proc.returncode)

for i in range(10, 15):
    os.spawnl(os.P_WAIT, "C:/GNURadio-3.7\\bin\\run_gr.bat", f"C:/GNURadio-3.7\\bin\\run_gr.bat C:/GNURadio-3.7\\bin\\uhd_rx_cfile.py test_{i+1}.bin -s -f 100000000 -r 1000000 -N 1024")

print("+++++++++++++++++++++++")
# a = input()
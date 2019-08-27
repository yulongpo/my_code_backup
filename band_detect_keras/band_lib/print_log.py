# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 15:42:17 2019

@author: huanghao
"""

import os

class Print_log(object):
    def __init__(self, log_file_path=None):
        self.log_file_path = log_file_path
        self.log_exists_checked = False
        
    def print_log(self, value="", log_file_path=None, print_flg=True):
        """
        * 输出到stdOut和日志
        
        * @value: 将要输出的内容
        * @log_file_path: 日志文件路径
        
        *return
        """
        if print_flg:
            print(value)
        
        if log_file_path is None:
            return
        
        self.log_file_path = log_file_path
        if not self.log_exists_checked:
            self.log_exists_checkout()
        with open(self.log_file_path, "a") as f:
            print(value, file=f)
        
    def log_exists_checkout(self):
        """
        * 检查日志文件是否存在
        """
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)
        self.log_exists_checked = True
        
    
print_log = Print_log().print_log

    
if __name__ == "__main__":
    print_log(1234, "test.log")
    print_log(4567, "test.log")
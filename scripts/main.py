import sys
from PyQt5.QtWidgets import QApplication
from AppGUI import AppGUI
import subprocess

if __name__ == '__main__':
    command = ['move', '/-Y', 'D:\\BaiduNetdiskDownload\\test.txt', 'D:\\']
    print(" ".join(command))
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    stdout, stderr = process.communicate()
    print(stdout)
    print(stderr)
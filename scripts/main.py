import sys
from PyQt5.QtWidgets import QApplication
from AppGUI import AppGUI
import threading

if __name__ == '__main__':
    # 在主线程中运行PyQt5界面
    app = QApplication(sys.argv)
    ex = AppGUI()
    ex.show()
    sys.exit(app.exec_())
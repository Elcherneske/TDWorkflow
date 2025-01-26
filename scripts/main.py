import sys
from PyQt5.QtWidgets import QApplication
from AppGUI import AppGUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppGUI()
    ex.show()
    sys.exit(app.exec_())
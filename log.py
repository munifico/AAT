import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import datetime
from kiwoom import *
import os
from manual_trading import *


form_class = uic.loadUiType("log.ui")[0]
SECU_BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),"security_file")

class Log(QWidget,form_class):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Log()
    main_window.show()
    app.exec_()
    app = None
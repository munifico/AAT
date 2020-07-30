import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import datetime
from kiwoom import *
import os
from config.log_class import *
from datetime import datetime
from PyQt5.QtCore import *

form_class = uic.loadUiType("log.ui")[0]
SECU_BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),"security_file")

class Log(QWidget,form_class):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)
        self.last_start_point = 0

        self.timer_0 = QTimer(self)
        self.timer_0.start(1000*1)
        self.timer_0.timeout.connect(self.log_check)



    def open_file(self):
        LOG_BASE_FILE = "log/" + "{:%Y-%m-%d}.log".format(datetime.now())
        with open(LOG_BASE_FILE, 'r+', encoding='utf-8') as f_read:
            data = f_read.readlines()
            # print(data)
        return data

    def find_last(self, system_log_list):
        len_system_log = len(system_log_list)
        count_start_point = []

        for i in range(len_system_log):
            if system_log_list[i][-21:-1] == "Kiwoom() class start":
                count_start_point.append(i)

        return count_start_point[-1]

    def log_check(self):
        system_log_list = self.open_file()

        if self.last_start_point == 0:
            self.last_start_point = self.find_last(system_log_list=system_log_list)

        # len_now_log = len(system_log_list) - self.last_start_point
        self.plainTextEdit_2.clear()

        for i in range(self.last_start_point, len(system_log_list)):
            self.plainTextEdit_2.appendPlainText(system_log_list[i])

        print(system_log_list[self.last_start_point:])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Log()
    main_window.show()
    app.exec_()
    app = None
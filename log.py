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
        self.kiwoom_last_start_point = 0
        self.trading_last_start_point = 0

        self.timer_0 = QTimer(self)
        self.timer_0.start(1000*1)
        self.timer_0.timeout.connect(self.log_check)

    def open_file(self):
        now = datetime.now().strftime("%Y-%m-%d")
        name_list = ["kiwoom", "trading"]
        LOG_BASE_FILE = []
        data = []

        for i, name in enumerate(name_list):
            LOG_BASE_FILE.append("log/{:s}.log".format(name))

            try:
                with open(LOG_BASE_FILE[i], 'r+', encoding='utf-8') as f_read:
                    data.append(f_read.readlines())
                    # print(data)

            except:
                with open(LOG_BASE_FILE[i], 'w+', encoding='utf-8') as f_write:
                    data.append("0")

        return data

    def find_last(self, system_log_list):
        len_system_log = len(system_log_list)
        count_start_point = []

        if system_log_list != "0":
            for i in range(len_system_log):
                if system_log_list[i][-21:-1] == "Kiwoom() class start":
                    count_start_point.append(i)

                if system_log_list[i][-22:-1] == "Trading() class start":
                    count_start_point.append(i)

                    if len_system_log > count_start_point[-1]:
                        count_start_point = []
                        break

            if len(count_start_point) == 0:
                return len_system_log
            return count_start_point[-1]

        elif system_log_list == "0":
            return len_system_log

    def log_check(self):
        system_log_list = self.open_file()

        if len(system_log_list[0]) != 0:
            if self.kiwoom_last_start_point == 0:
                self.kiwoom_last_start_point = self.find_last(system_log_list=system_log_list[0])

            self.plainTextEdit_2.clear()

            for i in range(self.kiwoom_last_start_point, len(system_log_list[0])):
                system_log = system_log_list[0][i][:-1]
                self.plainTextEdit_2.appendPlainText(system_log)

        if len(system_log_list[1]) != 0:
            if self.trading_last_start_point == 0:
                self.trading_last_start_point = self.find_last(system_log_list=system_log_list[1])

            self.plainTextEdit_4.clear()

            for i in range(self.trading_last_start_point,len(system_log_list[1])):
                system_log = system_log_list[1][i][:-1]
                self.plainTextEdit_4.appendPlainText(system_log)

            # len_now_log = len(system_log_list) - self.last_stat_point

        # print(system_log_list[self.kiwoom_last_start_point:])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Log()
    main_window.show()
    app.exec_()
    app = None
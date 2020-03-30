import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import datetime
from kiwoom import *
import requests
from bs4 import BeautifulSoup
import os

form_class = uic.loadUiType("main.ui")[0]
SECU_BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),"security_file")

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.non_login_state = True
        self.kiwoom = Kiwoom()

        self.holidays = self.open_api_holiday()

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.display_time)

        self.pushButton_2.clicked.connect(self.button_clicked)

    def display_time(self):
        today_time = datetime.datetime.today().strftime('%Y-%m-%d / %p.%H:%M:%S')

        self.label.setText(today_time)

        week = int(datetime.datetime.today().strftime('%w'))
        day = int(datetime.datetime.today().strftime('%d'))
        hour = int(datetime.datetime.today().strftime('%H'))
        min = int(datetime.datetime.today().strftime('%M'))

        if week == 6 or week == 0:
            self.label_2.setText("주말 입니다.")
            self._open_close(False)
        elif hour < 9 or ((hour >= 15) and (min > 30)):    # 9 - 15:30
            self.label_2.setText("개장 시간이 아닙니다.")
            self._open_close(False)
        elif day in self.holidays:
            self.label_2.setText("휴무일 입니다.")
            self._open_close(False)
        else:
            self.label_2.setText("장 오픈 !")
            self._open_close(True)

        self.connect_state()

        if hour == 8 and min == 50 and self.non_login_state:
            self.button_clicked()
            self.non_login_state = False

    """
    공공 데이터로 공휴일 처리
    개장 폐장은 하루 한번만 확인해도 됨
    프로그램 실행 때 딱 한번만 확인
    """
    def open_api_holiday(self):
        holi_api = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/"
        operation = "getHoliDeInfo"
        year = "?solYear=" + datetime.datetime.today().strftime('%Y')
        month = "&solMonth=" + datetime.datetime.today().strftime('%m')
        # month = "&solMonth=04"
        service_key = self.open_file()
        service_key = "&ServiceKey="+service_key

        url = holi_api+operation+year+month+service_key

        holiday_req = requests.get(url=url)
        holiday_xml = holiday_req.text

        soup = BeautifulSoup(holiday_xml, "xml")
        holidays = soup.find_all("locdate")

        holiday_day = []

        for holiday in holidays:
            holiday_slice = holiday.text
            holiday_slice = holiday_slice[6:8]
            holiday_day.append(holiday_slice)
        print("open_api_hoilday")
        return holiday_day

    def open_file(self):
        with open(os.path.join(SECU_BASE_DIR, "key.txt"),'r+', encoding='utf-8') as f_read:
            service_key = f_read.readline()
        return service_key

    def _open_close(self, door):
        if door == True:
            self.radioButton.setChecked(True)
            self.radioButton.setStyleSheet("Color : Blue")
            self.label.setStyleSheet("Color : Blue")

            self.radioButton_2.setStyleSheet("Color : Black")
        elif door == False:
            self.radioButton_2.setChecked(True)
            self.radioButton_2.setStyleSheet("Color : Red")

            self.radioButton.setStyleSheet("Color : Black")
            self.label.setStyleSheet("Color : Black")
        else:
            pass

    def connect_state(self):
        state = self.kiwoom.get_connect_state()

        if state == 1:
            self.label_3.setText("서버 연결 상태 😁")
            self.label_3.setStyleSheet("Color : Blue")
        elif state == 0:
            self.label_3.setText("서버 미연결 상태 😅")
            self.label_3.setStyleSheet("Color : Black")

    def button_clicked(self):
        self.kiwoom.comm_connect()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
    app = None
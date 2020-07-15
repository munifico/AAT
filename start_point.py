import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import datetime
from kiwoom import *
import requests
from bs4 import BeautifulSoup
import os
# from trading import *


form_class = uic.loadUiType("start.ui")[0]
SECU_BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),"security_file")

class Start(QWidget,form_class):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)
        self.login_state = False
        self.kiwoom = Kiwoom()

        """
        공휴일 api의 속도가 너무 느려져서 사용 불가능한 상황에 옴.
        따로 공휴일 리스트를 만들어서 사용해야 할듯
        일단 아래 open_api_holiday()는 사용 중지
        """
        # self.holidays = self.open_api_holiday()

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.display_time)

        # layout = QVBoxLayout()
        # layout.addWidget(self.groupBox)
        # layout.addWidget(self.groupBox_2)
        # layout.addWidget(self.groupBox_3)
        # self.setLayout(layout)


        self.pushButton_2.clicked.connect(self.button_clicked)

        # self.
        # self.open = False

        # parent.pushButton_2.clicked.connect(parent.button_clicked)

        # self.auto_trading_action.triggered.connect(lambda: self.show_sub_windows(self.auto_trading_action.text()))
        # self.manual_trading_action.triggered.connect(lambda: self.show_sub_windows(self.manual_trading_action.text()))
        # self.setGeometry(885,520,0 ,0)
        # self.move(885, 520)
        # self.resize(650, 450)

    # def show_sub_windows(self, action):
    #     if action == self.auto_trading_action.text():
    #         pass
    #         # self.auto_trading = AutoTrading()
    #         # self.auto_trading.show()
    #     elif action == self.manual_trading_action.text():
    #         # self.manual_trading = ManualTrading(self.state)
    #         self.manual_trading = ManualTrading(self.kiwoom, self.state)
    #         self.manual_trading.show()
    #
    #     # if self.action.isCheckable():
    #     #     print("A")
    #     # elif self.action_2.isChecked():
    #     #     print("B")
    #     # print(self.action.isEnabled())
    #     # print(self.action_2.isEnabled())

    def display_time(self):
        today_time = datetime.datetime.today().strftime('%Y-%m-%d / %p.%H:%M:%S')

        self.label.setText(today_time)

        month = int(datetime.datetime.today().strftime('%m'))
        week = int(datetime.datetime.today().strftime('%w'))
        day = datetime.datetime.today().strftime('%d')
        hour = datetime.datetime.today().strftime('%H')
        min = datetime.datetime.today().strftime('%M')

        hour_P_min = hour + min

        close_market = (6*60) + 30
        now_time = (int(hour) * 60) + int(min) - (9 * 60)
        open_close_per = (int(now_time) / close_market) * 100
        print(open_close_per)
        if(0 <= open_close_per and open_close_per <= 100):
            self.progressBar.setValue(open_close_per)
        elif(0 > open_close_per or open_close_per > 100):
            self.progressBar.reset()
        # print(self.holiday(month))

        if week == 6 or week == 0:
            self.label_2.setText("주말 입니다.")
            self._open_close(False)
        # elif day in self.holidays:
        #     self.label_2.setText("휴무일 입니다.")
        #     self._open_close(False)
        elif day in self.holiday(month):
            self.label_2.setText("공휴일 입니다")
            self._open_close(False)
        elif int(hour) < 9 or (int(hour_P_min) > 1530):    # 9 - 15:30 # 일단 이렇게 보류 / 더 나은 방법 찾아보기
            self.label_2.setText("개장 시간이 아닙니다.")
            self._open_close(False)
        else:
            self.label_2.setText("장 오픈 !")
            self._open_close(True)

        self.connect_state()

        if int(hour) == 8 and int(min) == 50 and self.non_login_state:
            self.button_clicked()
            self.non_login_state = False

    def holiday(self, M):
        holiday_2020_tuple = ((1, 23, 24, 25, 26, 27),
                         (),
                         (1),
                         (8),
                         (5),
                         (6),
                         (),
                         (15),
                         (30),
                         (1, 2, 3, 4, 9),
                         (),
                         (25))
        D = holiday_2020_tuple[M-1]
        print(D)
        return holiday_2020_tuple[M-1]


    """
    공공 데이터로 공휴일 처리
    개장 폐장은 하루 한번만 확인해도 됨
    프로그램 실행 때 딱 한번만 확인
    """
    # def open_api_holiday(self):
    #     holi_api = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/"
    #     operation = "getHoliDeInfo"
    #     year = "?solYear=" + datetime.datetime.today().strftime('%Y')
    #     month = "&solMonth=" + datetime.datetime.today().strftime('%m')
    #     # month = "&solMonth=04"
    #     service_key = self.open_file()
    #     service_key = "&ServiceKey="+service_key
    #
    #     url = holi_api+operation+year+month+service_key
    #
    #     holiday_req = requests.get(url=url)
    #     holiday_xml = holiday_req.text
    #     # print(holiday_xml)
    #     soup = BeautifulSoup(holiday_xml, "xml")
    #     holidays = soup.find_all("locdate")
    #
    #     holiday_day = []
    #
    #     for holiday in holidays:
    #         holiday_slice = holiday.text
    #         holiday_slice = holiday_slice[6:8]
    #         holiday_day.append(holiday_slice)
    #     print("open_api_hoilday")
    #     print(holiday_day)
    #     return holiday_day

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
            # if self.open != door:
            #     QMessageBox.about(self, "장 오픈", "지금부터 장이 열립니다")
            #     self.open == door

        elif door == False:
            self.radioButton_2.setChecked(True)
            self.radioButton_2.setStyleSheet("Color : Red")

            self.radioButton.setStyleSheet("Color : Black")
            self.label.setStyleSheet("Color : Black")
            # QMessageBox.about(self, "장 마감", "지금은 장이 마감상태입니다.")
        else:
            pass

    def connect_state(self):
        self.state = self.kiwoom.get_connect_state()

        if self.state == 1:
            self.label_3.setText("서버 연결 상태 😁")
            self.label_3.setStyleSheet("Color : Blue")
            self.login_state = True
        elif self.state == 0:
            self.label_3.setText("서버 미연결 상태 😅")
            self.label_3.setStyleSheet("Color : Black")

    def button_clicked(self):
        self.kiwoom.comm_connect()
        # self.manual_trading_action.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Start()
    main_window.show()
    app.exec_()
    app = None
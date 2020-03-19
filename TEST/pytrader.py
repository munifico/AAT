"""
현재 시간을 출력하는 기능은 일정한 단위로 현재 시간을 얻어온 후 이를 StatusBar에 출력.
이를 위해서는 주기적으로 이벤트를 발생시키는 Timer가 필요.
Timer가 1초에 한 번 이벤트(시그널)을 발생시키면 이 이멘트를 처리하는 메서드(슬롯)에서 현재 시간을 얻어온 후 이를 StatusBar에 출력

Qt 의 QTimer 클래스를 사용하면 정해진 시간마다 이벤트를 발생시킬 수 있다.
QTimer 클래스
메서드 start - 이 메서드에 인자로 1000을 지정하면 1초에 한 번씩 주기적으로 timeout 시그널이 발생.

시그널을 처리할 슬롯에서는.
timeout 메서드에서는 현재 시간을 구하고, 시간:분:초 형태의 문자열로 변환.
Kiwoom 클래스의 get_connect_state 메서드를 호출해서 서버 연결 상태를 확인한 후
시간과 상태 출력 메시지를 StatusBar 위젯에 출력.

키움 OpenAPI는 비밀번호를 저장받아서 자동 로그인이 된다.
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Kiwoom import *

form_class = uic.loadUiType("pytrader.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)

    def timeout(self):
        current_time = QTime.currentTime()
        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time

        state = self.kiwoom.get_connect_state()
        if state == 1:
            state_msg = "서버 연결 중"
        else:
            state_msg = "서버 미 연결 중"

        self.statusbar.showMessage(state_msg + " | " + time_msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
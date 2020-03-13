"""
복잡한 UI를 구성할 때는 UI 구성을 위한 전용 툴인 Qt Designer를 사용하는 것이 편리.
Qt Designer는 Qt의 컴포넌트를 이용해 GUI를 설계하는 전용 툴.
Qt Designer는 프로그래머가 GUI 구성을 위지위그(WYSIWYG: What You See Is What You Get) 방식으로 수행할 수 있도록 지원.

GUI 프로그램의 코드
1. GUI 레이아웃
2. 시그널-슬롯 연결 및 슬롯 처리 함수(메서드)
3. 이벤트 루프

2번은 구현 필수
But 1번은 Qt Designer가 위지위그 방식으로 UI 구성을 도와줌
"""

"""
Qt Designer로 UI를 만들고 .ui 파일을 열어보면
UI 레이아웃이 XML 형식으로 저장된걸 확인 가능.
"""

"""
1.
Qt Designer의 결과 파일인 UI 파일은 XML 언어로 구성.
파이썬은 XML을 바로 실행할 수 없으므로 XML 코드를 파이썬 코드로 변환해야한다.
'C:\\Anaconda3\\Lib\\site-packages\\PyQt5\\uic로 복사
uic 디렉터리에서 명령창 실행.
python -m PyQt5.uic.pyuic -x 파일명.ui -o 파일명.py

"""

"""
 2.
UI 파일을 파이썬 코드로 변환하지 않고 사용하는 방법.

파이썬 코드 안에 Ui 파일(XML 코드)를 파이썬 코드로 변환하는 모듈 추가해서 컨트롤 하기.
MyWindow는 다중 상속.
form_class는 my_window.ui 파일을 로드해서 만든 클래스

form_class를 상속받아서 form_class에 정의돼 있던 속성이나 메서드를 모두 상속.
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("my_window.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

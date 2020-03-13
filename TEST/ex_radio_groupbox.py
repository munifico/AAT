"""
QRadioButton은 사용자로부터 여러 가지 옵션 중 하나를 입력받을 때 사용.
QGroupBox는 제목이 있는 네모 박스 형태의 경계선을 만드는 데 사용.
"""

"""
QGroupBox 위젯을 이용해 '시간 단위'인 네모 박스를 만든다.
출력 위치 설정 move 메서드 호출
크기 조절 resize 메서드 호출 (width, heigh) (너비, 높이)

라디오 버튼도 QRadioButton 클래스의 생성자를 호출함으로써 객체를 생성.
인자값 = 1. 출력될 문자열, 2. 위젯이 출력될 부모 위젯
move 메서드로 출력 위치 설정.
setChecked 메서드는 라디오 버튼의 초기 상태를 설정.
True로 설정하는 경우 해당 라디오 버튼은 선택된 상태로 출력
clicked 시그널이 있다. 슬롯 설정 가능
"""
import sys
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)

        groupBox = QGroupBox("시간 단위", self)
        groupBox.move(10, 10)
        groupBox.resize(280, 80)

        self.radio1 = QRadioButton("일봉", self)
        self.radio1.move(20, 20)
        self.radio1.setChecked(True)
        self.radio1.clicked.connect(self.radioButtonClicked)

        self.radio2 = QRadioButton("주봉", self)
        self.radio2.move(20, 40)
        self.radio2.clicked.connect(self.radioButtonClicked)

        self.radio3 = QRadioButton("월봉", self)
        self.radio3.move(20, 60)
        self.radio3.clicked.connect(self.radioButtonClicked)

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("일봉 선택됨")

    def radioButtonClicked(self):
        msg = ""
        if self.radio1.isChecked():
            msg = "일봉"
        elif self.radio2.isChecked():
            msg = "주봉"
        else:
            msg = "월봉"
        self.statusBar.showMessage(msg + "선택 됨")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
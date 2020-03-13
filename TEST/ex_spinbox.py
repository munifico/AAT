"""
QSpinBox 위젯

QSpinBox 위젯을 보면 값을 증가시키는 데 사용하는 화살표, 값을 감소시킬 때 사용하는 화살표, 값을 출력하는 부분으로 구성.
"""

"""
생성자를 호출해 QSpinBox 클래스에 대한 인스턴스를 생성.
인자값 1. 부모.
move 메서드 출력 위치
resize 메서드 크기 조절

시그널
valueChanged -> QSpinBox의 값이 변경될 때 자동으로 발생하는 시그널 -> 슬롯 연결
QSpinBox의 value 메서드 -> 값을 얻어오기(정수) -> 문자열로 변경 후 QStatusBar 객체에 출력
    -> .setValue -> 초기값 설정.
    -> .setSingleStep -> 증가 / 감소 하는 값 설정. 
    -> .setMinimum -> 값의 범위 지정 (최솟값)
    -> .setMaximum -> 최댓값
"""
import sys
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)

        label = QLabel("매도 수량: ", self)
        label.move(10, 20)

        self.spinBox = QSpinBox(self)
        self.spinBox.move(70, 25)
        self.spinBox.resize(80, 22)
        self.spinBox.valueChanged.connect(self.spinBoxChanged)

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def spinBoxChanged(self):
        val = self.spinBox.value()
        msg = '%d 주를 매도합니다.' %(val)
        self.statusBar.showMessage(msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
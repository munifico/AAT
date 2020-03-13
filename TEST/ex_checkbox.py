"""
QCheckBox 위젯

QRadioButton 위젯과 달리 여러 옵션을 동시에 선택 가능.
"""

"""
CheckBox를 사용하려면 QCheckBox 클래스의 인스턴스를 생성.
인자값 = 1. 표시될 텍스트, 2. 부모 위젯.
QCheckBox는 QMainWindow 객체 안에 출력되기 때문에 부모 위젯으로 self를 사용.

QCheckBox 클래스는 QRadioButton 클래스와 마찬가지로 move와 resize라는 메서드를 가짐.
move 메서드를 통해 출력될 위치 설정.
resize 메서드를 통해 크기를 지정

QCheckBox 위젯을 self.checkBox 인스턴스 변수가 바인딩.

QCheckBox가 선택될 때 어떤 QCheckBox가 선택되었는가에 대한 정보를 출력할 용도로 QStatusBar 위젯도 생성.

QCheckBox는 CheckBox가 선택되지 않은 상태에서 선택되거나 / 선택된 상태에서 선택 해제가 된 경우에 stateChanged라는 시그널을 발생.
QCheckBox 위젯의 상태를 변경할 때 이를 처리하는 함수인 슬롯 -> stateChanged 시그널

isChecked 메서드를 통해 QCheckBox 위젯 객체가 선택된 상태인지 확인할 수 있음.

"""
import sys
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)

        self.checkBox1 = QCheckBox("5일 이평선", self)
        self.checkBox1.move(10,20)
        self.checkBox1.resize(150,30)
        self.checkBox1.stateChanged.connect(self.checkBoxState)

        self.checkBox2 = QCheckBox("20일 이평선", self)
        self.checkBox2.move(10,50)
        self.checkBox2.resize(150, 30)
        self.checkBox2.stateChanged.connect(self.checkBoxState)

        self.checkBox3 = QCheckBox("60일 이평선",self)
        self.checkBox3.move(10, 80)
        self.checkBox3.resize(150, 30)
        self.checkBox3.stateChanged.connect(self.checkBoxState)

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def checkBoxState(self):
        msg = ""
        if self.checkBox1.isChecked() == True:
            msg +="5일 "
        if self.checkBox2.isChecked() == True:
            msg += "20일 "
        if self.checkBox3.isChecked() == True:
            msg += "60일 "
        self.statusBar.showMessage(msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
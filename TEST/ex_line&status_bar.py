"""
QLineEdit 한 줄의 텍스트를 입력할 수 있는 위젯.
 사용자로부터 간단한 텍스트를 입력받을 때 사용.
"""

"""
QLineEdit을 이용해 사용자로부터 값을 입력받을 수 있다.
QLineEdit 객체의 시그널 중 적당한 시그널을 사용해 사용자 이벤트를 처리해야 한다.

표 16.1 자주 사용되는 QLineEdit 시그널

시그널	시그널 발생 시점
textChanged( )	QLineEdit 객체에서 텍스트가 변경될 때 발생
returnPressed( )	QLineEdit 객체를 통해 사용자가 엔터키를 눌렀을 때

QLineEdit에 입력된 값을 보여주기 위해 QStatusBar 위젯을 생성.
lineEditChanged 메서드에서는 self.statusBar라는 변수로 showMessage 메서드를 호출.
상태 표시줄에 텍스트를 출력.
출력될 문자열(.showMessage)는 QLineEdit 객체에 입력한 텍스트
-> self.lineEdit 변수를 통해 QLineEdit 객체에 접근한 후 text() 메서드를 통해 사용자가 입력한 문자열을 얻는다.
"""
import sys
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 400, 300, 150)

        # Label
        label = QLabel("종목코드", self)
        label.move(20, 20)

        # LineEdit
        self.lineEdit = QLineEdit("", self)
        self.lineEdit.move(80, 20)
        self.lineEdit.textChanged.connect(self.lineEditChanged)

        # StatusBar
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def lineEditChanged(self):
        self.statusBar.showMessage(self.lineEdit.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
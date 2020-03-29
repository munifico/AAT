"""
QLabel 위젯은 텍스트나 이미지를 출력하는 데 사용.
"""

"""
Message 텍스트를 출력하는 QLabel 객체는 textLabel 변수로 바인딩
버튼~ QLabel 객체는 self.label 변수로 바인딩

self.의 이유
생성한 위젯을 클래스 내의 다른 메서드에서 참조할 때는 변수 이름에 self를 붙여야 하고,
그렇지 않은 경우에는 self를 붙이지 않는다.
self를 붙이지 않고 메서드의 인자값으로 값을 보낼 수 있다.

QLabel 클래스의 인스턴스를 생성한 후에는
move 메서드를 통해 해당 객체가 출력되는 위치를 조정.
resize 메서드를 호출해 크기를 조정.

각 버튼의 이벤트를 적절히 처리하기 위해 각 버튼 위젯의 clicked 시그널을 self.btn~_clicked 슬롯과 연결했다.

.setText 메서드 = QLabel 객체에 텍스트 출력.
.clear 메서드 = 문자열 지우기
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("pytrader.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.setupUI()
        a = self.Form()
        a.show()
        self.pushButton

    def setupUI(self):
        self.setGeometry(800, 400, 300, 150)

        textLabel = QLabel("Message: ", self)
        textLabel.move(20, 20)

        self.label = QLabel("", self)
        self.label.move(100, 20)
        self.label.resize(200, 30)

        btn1 = QPushButton("click", self)
        btn1.move(20, 60)
        btn1.clicked.connect(self.btn1_clicked)

        btn2 = QPushButton("Clear", self)
        btn2.move(140, 60)
        btn2.clicked.connect(self.btn2_clicked)

    def btn1_clicked(self):
        self.label.setText("버튼이 클릭되었습니다.")
        self.a = Mywindow2()
        self.a.show()
        # a.exec_()

    def btn2_clicked(self):
        self.label.clear()

class Mywindow2(QWidget):
   def __init__(self):
       super().__init__()
       self.setupUI()

   def setupUI(self):
       self.setGeometry(800,400,300,100)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
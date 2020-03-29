"""
PyQt에서 UI를 구성하는 데 사용되는 요소를 위젯이라고 한다.
GUI 프로그래밍은 여러 위젯을 활용해 최적의 UI를 구성한 후 각 위젯에서 발생하는 이벤트를 적절히 처리하는 것.
"""

"""
QPushButton

UI를 구성할 때 가장 기본이 되는 위젯.
Y/N 같은 이벤트를 받는데 사용.
"""

"""
QCoreApplication.instance()를 이용하면 app 변수가 바인딩하고 있는 동일한 객체를 얻어올 수 있다.
app이 바인딩하고 있는 객체는 QApplication 클래스의 인스턴스인데 해당 객체는 quit라는 메서드를 포함.
"""
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setupUI()
#
#     def setupUI(self):
#         btn1 = QPushButton("닫기", self)
#         btn1.move(20, 20)
#         btn1.clicked.connect(QCoreApplication.instance().quit)
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     mywindow = MyWindow()
#     mywindow.show()
#     app.exec_()

"""
위와 동일한 코드지만 유지보수성이 낮다.
app 변수를 전역으로 선언해서 클래스 내에서도 app을 사용할 수 있다.
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

app = None

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        btn1 = QPushButton("닫기", self)
        btn1.move(20, 20)
        btn1.clicked.connect(app.quit)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()

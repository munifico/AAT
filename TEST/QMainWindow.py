import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MyWindow(QMainWindow):                    # QMainWindow를 상속 받음
    def __init__(self):
        super().__init__()                      # 부모의 __init__을 호출
        self.setWindowTitle("PyStock")          # 부모의 메서드 setWindowTitle 입력.
        self.setGeometry(300, 300, 300, 400)

        btn1 = QPushButton("Click me", self)    # QPushButton 클래스
        btn1.move(20,20)
        btn1.clicked.connect(self.btn1_clicked) # btn1_clicked가 argument를 안받고 함수 자체만 불러옴

    def btn1_clicked(self):
        QMessageBox.about(self, "message", "clicked")
        print("a")

    def a(self):
        print("b")

def func1(name):
    print("c")
    return(name())

def func2():
    return "D"


if __name__ == "__main__":
    print(func1(func2))


    # app = QApplication(sys.argv)
    # mywindow = MyWindow()
    # print(type(mywindow.btn1_clicked))
    # mywindow.show()
    # print(mywindow.a)
    # app.exec_()

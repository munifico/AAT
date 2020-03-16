"""
레이아웃
GUI 프로그램이에서 위젯을 배치하는 것
resize, move, setGeometry 메서드를 이용해 위젯의 출력 위치를 설정.

그러나 위 메서드를 사용해서 위젯의 크기와 출력 위치를 명시적으로 설정하는 방법은
윈도우 크기가 바뀔때 문제가 있다.
"""

# import sys
# from PyQt5.QtWidgets import *
#
# class MyWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setupUI()
#
#     def setupUI(self):
#         self.setGeometry(800, 200, 300, 300)
#
#         self.textEdit = QTextEdit(self)
#         self.textEdit.resize(280, 250)
#         self.textEdit.move(10, 10)
#
#         self.pushButton = QPushButton('저장', self)
#         self.pushButton.resize(280, 25)
#         self.pushButton.move(10, 270)
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     mywindow = MyWindow()
#     mywindow.show()
#     app.exec_()

"""
레이아웃 매니저

1) 위젯 만들기   (self.pushButton = QPushButton(""))
2) 레이아웃 매니저 만들기   (layout = 레이아웃 매니저())
3) addWidget 메서드를 이용한 위젯 등록    (layout.addWidget(self.pushButton))
4) 레이아웃 매니저 등록    (self.setLayout(layout))

레이아웃 매니저를 사용할 때
레이아웃 매니저에 추가되는 위젯을 생성할 때 인자값으로 부모 위젯을 지정할 필요가 없다.
위젯의 크기나 위치를 명시적으로 설정하지 않아야함.

QVBoxLayout 클래스 - 위젯을 수직 방향으로 나열

윈도우의 크기를 자유롭게 변경해도 내부 위젯이 일정한 비율을 가지며 크기가 자동으로 바뀐다.
"""

# import sys
# from PyQt5.QtWidgets import *
#
# class MyWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setupUI()
#
#     def setupUI(self):
#         self.setGeometry(800, 200, 300, 300)
#
#         self.textEdit = QTextEdit()
#         self.pushButton = QPushButton('저장')
#
#         layout = QVBoxLayout()
#         layout.addWidget(self.pushButton)
#         layout.addWidget(self.textEdit)
#
#         self.setLayout(layout)
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     mywindow = MyWindow()
#     mywindow.show()
#     app.exec_()

"""
QHBoxLayout 클래스 - 위젯을 행 방향으로 배치할 때 사용.


"""
#
# import sys
# from PyQt5.QtWidgets import *
#
# class MyWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setupUI()
#
#     def setupUI(self):
#         self.setGeometry(800, 200, 300, 100)
#
#         self.pushButton1 = QPushButton("Button1")
#         self.pushButton2 = QPushButton("Button2")
#         self.pushButton3 = QPushButton("Button3")
#
#         layout = QHBoxLayout()
#         layout.addWidget(self.pushButton1)
#         layout.addWidget(self.pushButton2)
#         layout.addWidget(self.pushButton3)
#
#         self.setLayout(layout)
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     mywindow = MyWindow()
#     mywindow.show()
#     app.exec_()

"""
QGridLayout 클래스 - 격자 형태의 UI를 구성하는 데 사용.

QGridLayout은 격자에서 위젯을 배치할 좌표를 입력 받는다.
addWidget 메서드에서 행과 열의 인덱스를 차례로 입력받는다.
각 행과 열에 대해 0부터 시작하는 정숫값을 통해 인덱싱.

아래 코드는 2x3 격자를 만든 것
"""

# import sys
# from PyQt5.QtWidgets import *
#
# class MyWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setupUI()
#
#     def setupUI(self):
#         self.setGeometry(800, 200, 300, 100)
#
#         self.label1 = QLabel("ID : ")
#         self.label2 = QLabel("PW: ")
#         self.lineEdit1 = QLineEdit()
#         self.lineEdit2 = QLineEdit()
#         self.pushButton1 = QPushButton("Sign In")
#
#         layout = QGridLayout()
#
#         layout.addWidget(self.label1, 0, 0)
#         layout.addWidget(self.lineEdit1, 0, 1)
#         layout.addWidget(self.pushButton1, 0, 2)
#
#         layout.addWidget(self.label2, 1, 0)
#         layout.addWidget(self.lineEdit2, 1, 1)
#
#         self.setLayout(layout)
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     mywindow = MyWindow()
#     mywindow.show()
#     app.exec()

"""
레이아웃 중첩

QVBoxLayout과 QHBoxLayout를 중첩
레이아웃 매니저 클래스에서 addWidget 메서드를 통해 레이아웃에 위젯을 추가하듯이.
addLayout 메서드를 호출하면 레이아웃에 다른 레이아웃 매니저를 추가할 수 있다.

QHBoxLayout 안에 두 개의 QVBoxLayout이 존재.

윈도우 왼쪽에는 QGroupBox와 QCheckBox 위젯이 위치.
위젯 생성시 크기나 좌표를 설정하지 않는다.

QGroupBox에 여러 개의 QCheckBox를 추가할 때
QVBoxLayout을 사용해 QCheckBox 위젯을 추가.

QVBoxLayout 객체에는 QCheckBox 위젯이 포함돼 있으므로 QGroupBOx에 QVBoxLayout 객체만 추가하면
QCheckBox를 QGroupBox 안쪽으로 배치 할 수 있다.

QGroupBox를 윈도우의 안쪽에 배치하기 위해 QVBoxLayout을 사용해 위젯을 추가

QTableWidget 객체를 윈도우의 오른쪽에 위치시키려면 QVBoxLayout 클래스의 객체를 생성.
QTableWidget 객체를 추가.

QHBoxLayout 클래스의 객체를 생성한 후 레이아웃을 추가.

현재 윈도우에 레이아웃을 layout 객체로 설정.
"""

import sys
from PyQt5.QtWidgets import *

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 500, 300)

        groupBox = QGroupBox("검색옵션")
        checkBox1 = QCheckBox("상한가")
        checkBox2 = QCheckBox("하한가")
        checkBox3 = QCheckBox("시가총액 상위")
        checkBox4 = QCheckBox("시가총액 하위")
        checkBox5 = QCheckBox("회전율 상위")
        checkBox6 = QCheckBox("대량거래상위")
        checkBox7 = QCheckBox("환산주가상위")
        checkBox8 = QCheckBox("외국인한도소진상위")
        checkBox9 = QCheckBox("투자자별순위")

        tableWidget = QTableWidget(10, 5)
        tableWidget.setHorizontalHeaderLabels(["종목코드", "종목명", "현개가", "등락률", "거래량"])
        tableWidget.resizeColumnsToContents()
        tableWidget.resizeRowsToContents()

        leftInnerLayOut = QVBoxLayout()
        leftInnerLayOut.addWidget(checkBox1)
        leftInnerLayOut.addWidget(checkBox2)
        leftInnerLayOut.addWidget(checkBox3)
        leftInnerLayOut.addWidget(checkBox4)
        leftInnerLayOut.addWidget(checkBox5)
        leftInnerLayOut.addWidget(checkBox6)
        leftInnerLayOut.addWidget(checkBox7)
        leftInnerLayOut.addWidget(checkBox8)
        leftInnerLayOut.addWidget(checkBox9)
        groupBox.setLayout(leftInnerLayOut)

        leftLayOut = QVBoxLayout()
        leftLayOut.addWidget(groupBox)

        rightLayOut = QVBoxLayout()
        rightLayOut.addWidget(tableWidget)

        layout = QHBoxLayout()
        layout.addLayout(leftLayOut)
        layout.addLayout(rightLayOut)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
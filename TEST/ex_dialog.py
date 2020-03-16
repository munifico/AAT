"""
다이얼로그는 '대화'라는 뜻을 가진 영어.
GUI 프로그래밍에서 다이얼로그는 사용자와의 상호작용을 위해 사용되는 윈도우를 의미.

"""

"""
파일 열기 창 - QFileDialog 클래스

메서드
getOpenFileName 
인자 1. 부모

반환된 파일 경로는 튜플 타입
label 객체의 setText 메서드를 통해 출력.
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
#         self.setWindowTitle("Pystock v0.1")
#
#         self.pushButton = QPushButton("File Open")
#         self.pushButton.clicked.connect(self.pushButtonClicked)
#         self.label = QLabel()
#
#         layout = QVBoxLayout()
#         layout.addWidget(self.pushButton)
#         layout.addWidget(self.label)
#
#         self.setLayout(layout)
#
#     def pushButtonClicked(self):
#         fname = QFileDialog.getOpenFileName(self)
#         self.label.setText(fname[0])
#         print(fname)
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     app.exec_()

"""
QInputDialog / 사용자로부터 간단한 텍스트, 정수, 실수를 받을 때 사용.

QInputDialog 클래스
메서드
getInt
인자 1. 부모, 2. QinputDialog 창에 표시될 텍스트, 3. QInputDialog 창 내부에 출력될 텍스트
getInt 메서드는 (text, ok) 튜플 형태로 값을 반환.
    text는 사용자가 입력한 값, ok는 사용자가 ok를 누른 경우 true

getDouble
실수를 입력시.

getText
문자열 입력시.

getItem
개발자가 생성한 옵션 중 하나를 선택 받고자 할 때.
인자 1. 부모, 2.다이얼로그의 타이틀 텍스트, 3. 내부 텍스트, 4. 선택할 아이템 리스트, 5. 초기 아이템 인덱스, 6. 아이템 수정 가능 여부(boolean)
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
#         self.setWindowTitle("PyStock v0.1")
#
#         self.pushButton = QPushButton("Input number")
#         self.pushButton.clicked.connect(self.pushButtonClicked)
#         self.label = QLabel()
#
#         layout = QVBoxLayout()
#         layout.addWidget(self.pushButton)
#         layout.addWidget(self.label)
#
#         self.setLayout(layout)
#
#     def pushButtonClicked(self):
#         text, ok = QInputDialog.getInt(self, "매수수량", "매수 수량을 입력하세요.")
#         if ok:
#             self.label.setText(str(text))
#
#     def pushButtonClicked1(self):
#         items = ("1","2","3")
#         item, ok = QInputDialog.getItem(self, "시장", "선택해", items, 0, False)
#         if ok and item:
#             self.label.setText(item)
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     app.exec_()

"""
한 개의 메인 윈도우와 다이얼로그로 구성된 프로그램.
다이얼로그 창은 .close() 메서드를 통해 종료 가능

pushButtonClicked 메서드에서는 앞서 정의한.
LogInDialog 클래스에 대한 인스턴스를 생성.
인스턴스의 메서드인 exec_를 호출
exec_ 메서드는 다이얼로그 창을 Modal 형태로 출력. (Modal 다이얼로그는 해당 다이얼로그 창을 닫을 때까지 부모 윈도우로 이동할 수 없다.)

"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class LogInDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.id = None
        self.password = None

    def setupUI(self):
        self.setGeometry(1100, 200, 300, 100)
        self.setWindowTitle("Sigh In")
        self.setWindowIcon(QIcon('icon.png'))

        label1 = QLabel("ID : ")
        label2 = QLabel("PW : ")

        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit()
        self.pushButton1 = QPushButton("S I")
        self.pushButton1.clicked.connect(self.pushButtonClicked)

        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.lineEdit1, 0, 1)
        layout.addWidget(self.pushButton1, 0, 2)
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.lineEdit2, 1, 1)

        self.setLayout(layout)

    def pushButtonClicked(self):
        self.id = self.lineEdit1.text()
        self.password = self.lineEdit2.text()
        self.close()

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle("PyStock v0.1")
        self.setWindowIcon(QIcon('icon.png'))

        self.pushButton = QPushButton("S I")
        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.label =QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.pushButton)
        layout.addWidget(self.label)

        self.setLayout(layout)


    def pushButtonClicked(self):
        dlg = LogInDialog()
        dlg.exec_()
        id = dlg.id
        password = dlg.password
        self.label.setText("ID: %s password :%s" % (id, password))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()


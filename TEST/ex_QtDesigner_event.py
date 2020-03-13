
"""
이벤트 처리하기

버튼 객체에 접근하기 위해 self.pushButton을 사용.
self.pushButton이라는 변수는 어떤 객체도 바인딩하고 있지 않다.
-> 버튼 객체에 대한 생성 및 바인딩은 setupUi 메서드에서 수행되기 때문.

Qt Designer를 실행한 후 main_window.ui 파일을 연다.
위젯을 클릭하고 Property Editor에서 objectName이 pushButton인 것을 확인.
이 값이 파이썬 코드에서 해당 객체에 접근하는데 사용됨.
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("my_window.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        QMessageBox.about(self, "message", "clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
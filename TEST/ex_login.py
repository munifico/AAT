import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 150)

        """
        고유의 CLSID 또는 ProgID를 가진다
        해당 값을 QAxWidget 클래스의 생성자로 전달하면 인스턴스가 생성된다.
        레지스트리 -> KHOPENAPI.KHOpenAPICtrl.1 -> CLSID -> {A1574A0D-6BFA-4BD7-9020-DED88711818D}        
        """
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        btn1 =QPushButton("Login", self)
        btn1.move(20, 20)
        btn1.clicked.connect(self.btn1_clicked)

        btn2 = QPushButton("Check stast", self)
        btn2.move(20, 70)
        btn2.clicked.connect(self.btn2_clicked)
        """
        OPEN API가 제공하는 메서드를 사용하려면 self.kiwoom 객체를 통해 dynamicCall 메서드를 호출해야 한다.
        dynamicCall 메서드의 인자로 호출하려는 메서드를 전달
        
        로그인 성공 또는 실패시 OnEventconnect 이벤트 발생
        
        키움 로그인 윈도우 생성
        계정 정보를 입력 후 로그인시 키움증권 서버에 로그인
        
        """
    def btn1_clicked(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")
        print(ret)
        """
        현재 접속 상태를 반환하는 GetConnectState 메서드 제공
        0 - 미연결
        1 - 연결완료
        
        self.statusBar() 어플리케이션의 상태를 알려주기 위해 하단에 위치하는 위젯
        .showMessage("") 상태바에 텍스트를 표시하기 위해 사용하는 메서드
        """
    def btn2_clicked(self):
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            self.statusBar().showMessage("Not connected")
        else:
            self.statusBar().showMessage("Connected")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow =MyWindow()
    myWindow.show()
    app.exec_()
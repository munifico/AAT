import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Kiwoom Login
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")

        # OpenAPI+ Event
        self.kiwoom.OnEventConnect.connect(self.event_connect)

        self.setWindowTitle("계좌 정보")
        self.setGeometry(300, 300, 300, 150)

        btn1 = QPushButton("계좌 얻기", self)
        btn1.move(190, 20)
        btn1.clicked.connect(self.btn1_clicked)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 60, 280, 80)
    """
    GetLoginInfo 메서드 = dynamicCall
    원형 = BSTR GetLoginInfo(BSTR sTag)
    반환값 = 계좌 갯수, 계좌 번호, 사용자 ID, 사용자명, 키보드보안 해지 여부, 방화벽 설정 여부
            ACCOUNT_CNT, ACCNO, USER_ID, USER_NAME, KEY_BSECGB, FIREW_SECGB
    
    GetLoginInfo 메서드의 인자가 한 개인데 실제 인자는 리스트 형태로 전달해야한다.
    인자로 ACCNO을 전달하면 서버는 전체 계좌를 반환한다.
    """
    def btn1_clicked(self):
        account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"])
        self.text_edit.append("계좌번호 : " + account_num.rstrip(';'))

    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append("로그인 성공")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
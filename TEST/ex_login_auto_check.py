import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 150)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")
        """
        클래스의 다른 메서드에서도 해당 변수를 사용해 객체에 접근하기 위해 self 사용
        읽기 / 쓰기 모드를 변경하기 위해 setEnabled 메서드 사용
        """
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 60, 280, 80)
        self.text_edit.setEnabled(False)
        """
        OnEventConnect 대소문자 주의
        
        통신 연결 상태가 바뀔 때 OnEventConnect라는 이벤트가 발생
        발생된 OnEventconnect 이벤트를 처리하기 위해 MyWindow 클래스에 event_connect라는 메서드 구현
        이벤트와 이벤트 처리 메서드만 연결하면 이벤트(OnEventConnect) 발생시 자동으로 이벤트 처리 메서드(self.event_connect) 호출
        
        OnEventConnect는 void OnEventConnect(LONG nErrCode):로 정의되어 있다.
        인자값 Long nErrCode는 0이면 로그인 성공, 음수면 실패
        
        Open API+의 이벤트를 처리하려면 이벤트 함수의 원형을 참조해서 해당 이벤트를 처리할 메서드 구현
        """
        self.kiwoom.OnEventConnect.connect(self.event_connect)

    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append("로그8인 성공")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

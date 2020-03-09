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
        """
        OnReceiveTrData 이벤트를 처리할 receive_trdata 메서드 구현.
        이벤트와 이벤트 처리 메서드를 연결. connect
        """
        # OpenAPI+ Event
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)


        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 150)
        """
        QLabel은 텍스트나 이미지를 출력하는데 사용
        첫 번째 인자 = 출력될 문자열
        두 번째 인자 = 부모 위젯

        위젯 출력 위치를 조절하기 위해 move 메서드 사용
        크기와 위치를 동시에 조절하려면 setGeometry 메서드 사용
        
        QLabel은 텍스트를 출력하는 용도로만 사용
        self 없이 label로 바인딩
        """
        label = QLabel('종목코드: ', self)
        label.move(20, 20)
        """
        사용자로부터 입력받기 위해 QLineEdit 위젯 사용
        setText로 기본값 설정
        """
        self.code_edit = QLineEdit(self)
        self.code_edit.move(80, 20)
        self.code_edit.setText("039490")
        """
        버튼의 이벤트를 처리하기 위해 btn1 객체에서 clicked 이벤트가 발생하면 btn1_clicked 메서드가 호출
        
        한 위젯에서 이벤트 발생시 다른 위젯으로부터 값을 읽고 이를 처리한 후 또 다른 위젯에 값을 출력
        GUI 프로그래밍에서 일반적임.
        """
        btn1 = QPushButton("조회", self)
        btn1.move(190, 20)
        btn1.clicked.connect(self.btn1_clicked)
        """
        로그인 처리 결과 / Open API+ 결과를 출력하기 위해 QTextEdit 위젯 사용
        사용자가 QTextEdit 위젯을 통해 읽기 모드로만 사용하도록 setEnabled 메서드를 사용
        """
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 60, 280, 80)
        self.text_edit.setEnabled(False)

    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append("로그인 성공")

    def btn1_clicked(self):
        code = self.code_edit.text()
        self.text_edit.append("종목코드 : " + code)
        """
        사용자가 입력한 종목 코드값으로 TR 데이터를 구성하고, 해당 TR을 서버로 송신하도록 코드를 수정.
        
        CommRqData
        첫 번째 인자는 사용자가 TR을 구분하기 위한 용도로 사용.   / 사용자가 지정 가능
        두 번째 인자는 요청하는 TR 이름으로 "opt10001" 입력.
        세 번째 인자로 단순 조회일 경우 0
        네 번째 인자는 4자리의 화면번호  / 기본값 0101
        """
        # SetInputValue
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)

        # CommRqData
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")

    """
    OnReceiveTrData 이벤트
    void OnReceiveTrData(~) 원형
    이 이벤트는 서버와 통신한 후 서버로부터 데이터를 전달받은 시점에 발생
    (LPCTSTR sScrNo, LPCTSTR sRQName, LPCTSTR sTrCode, LPCTSTR sRecordName,
     LPCTSTR sPreNext, LONG nDataLength, LPCTSTR sErrorCode, LPCTSTR sMessage, LPCTSTR sSplmMsg)
     이 9개의 인자 전달.
     
     OnReceiveTrData 이벤트가 발생했다는 것은 서버로부터 데이터를 전달 받았음을 의미
     OnReceiveTrData 메서드에서 CommGetData 메서드를 호출해서 데이터를 가져오면 됨.
     TR 데이터, 실시간 데이터, 체결잔고 데이터 등을 구할 수 있다.
     
     CommGetData 메서드는 Open API+에서 제공하는 메서드
     파이썬에서 사용하려면 dynamicCall 메서드를 사용해야 함.
     첫 번째 인자는 TR명
     세 번째 인자는 Request명 (Rqname)
     
     receive_trdata 메서드는 OnReceiveTrData 이벤트가 발생할 때마다 자동으로 호출
     어떤 TR 요청에 의해 OnReceiveTrData 이벤트가 발생했는지 확인하기 위해 사용자 Rqname을 확인
     
     CommGetData는 일부 함수에서 작동이 안된다고 한다.
     개발 가이드에도 아래를 권장한다.
     조회 정보 요청 GetCommData(trcode, rqname, 0, '현재가')
     실시간 정보 요청 GetCommRealData("000660", 10)
     체결 정보 요청 GetChejanData(9203)
    """
    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        if rqname == "opt10001_req":
            # name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목명")
            # volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "거래량")
            name = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "종목명")
            volume = self.kiwoom.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, 0, "거래량")
            # a = self.kiwoom.dynamicCall("GetCommRealData(QString, int)", "000660", 10)

            self.text_edit.append("종목명: " + name.strip())
            self.text_edit.append("거래량: " + volume.strip())
            # self.text_edit.append(("실시간 : " + a.strip()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

"""
Open API+의 TR 처리 순서

1) SetInputValue 메서드를 사용해 TR 입력 값을 설정.
2) CommRqData 메서드를 사용해 TR을 서버로 송신
3) 서버로부터 이벤트가 발생할 때까지 이벤트 루프를 사용해 대기
4) CommGetData 메서드를 사용해 수신 데이터를 가져온다.
"""
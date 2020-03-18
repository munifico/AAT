"""
GetCodeListByMarket 메서드 - 각 시장에 속하는 중목의 종목 코드 리스트를 얻을 수 있다.
bstr GetCodeListByMarket(LPCTSTR sMarket)
 인자 - 시장 구분 - 0:장내, 3:ELW, 4:뮤추얼펀드, 5:신주인수권, 6:리츠,
                8:ETF, 9:하이일드펀드, 10:코스닥, 30:K-OTC, 50:코넥스(KONEX)
 반환값 - 종목 코드 리스트, 종목간 구분은 ';'이다.

메서드 이름에 _(언더스코어)를 붙인 이유는 주로 자신이 속한 클래스의 메서드에서 호출되기 때문.

키움증권은 로그인 요청을 받으면 OnEventConnect 이벤트 발생 시그널 -> 슬롯 _event_connet과 연결

GetCodeListByMarket 메서드를 호출하기 위해 dynamicCall 메서드 사용

QEveentLoop()를 통해 이벤트 루프를 생성.

Kiwoom 클래스는 QAxWidget 클래스를 상속받았기 때문에
Kiwoom 클래스에 대한 인스턴스를 생성하려면 먼저 QApplication 클래스의 인스턴스를 생성해야 한다.
그 다음 Kiwoom 클래스에 대한 인스턴스를 생성할 수 있다.

맨 마지막 줄 app = None 이 없으면
Process finished with exit code -1073741819 (0xC0000005)
메모리 오류가 뜬다.

GetMasterCodeName 메서드 - 종목 코드로 한글 종목명을 얻어온다.
 인자 - 종목 코드
 반환값 - 종목 한글명
 
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()
    code_list = kiwoom.get_code_list_by_market('10')

    for code in code_list:
        print(code, end=' ')
        print(kiwoom.get_master_code_name(code), end=' ')

    app = None

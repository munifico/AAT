"""
일봉 데이터 연속 조회
키움 OpenAPI+를 통해 일봉 데이터를 얻을 수 있다.
opt10081 - TR

OpenAPI+가 제공하는 TR을 사용하려면 SetInputValue 메서드를 통해 요청하는 TR에 필요한 데이터를 설정한 후
CommRqData 메서드를 호출해 TR을 키움증권 서버로 전송한다.
TR 요청받은 서버는 이를 처리한 후 데이터가 준비되면 이벤트를 발생시켜 사용자가 데이터를 가져갈 수 있게 알려준다.

SetInputValue 메서드 - Tran 입력 값을 서버 통신 전에 입력한다.
 void SetInputValue(BSTR sID, BSTR sValue)
 인자값 = sID - 아이템 명, sValue - 입력 값
 반환값 = x

CommRqData 메서드 - Tran을 서버로 송신한다.
 LONG CommRqData(BSTR sRQName, BSTR sTrCode, long nPrevNext, BSTR sScreenNo)
 인자값 = sRQName – 사용자구분 명
        sTrCode - Tran명 입력
        nPrevNext - 0:조회, 2:연속
        sScreenNo - 4자리의 화면번호
 반환값 = OP_ERR_SISE_OVERFLOW – 과도한 시세조회로 인한 통신불가
        OP_ERR_RQ_STRUCT_FAIL – 입력 구조체 생성 실패
        OP_ERR_RQ_STRING_FAIL – 요청전문 작성 실패
        OP_ERR_NONE – 정상처리

CommRqData를 통해 키움증권 서버에 TR을 요청하면 데이터가 바로 반환되는 것이 아니다.
키움증권 서버는 TR을 처리한 후 이벤트를 통해 알려주기 때문에.
이벤트를 줄 때까지 대기해야 한다.
때문에 CommRqData를 호출한 후에 이벤트 루프를 만들어주는 코드가 반드시 있어야 한다.

GetRepeatCnt 메서드 - 레코드의 반복횟수를 반환한다.
 LONG GetRepeatCnt(LPCTSTR sTrCode, LPCTSTR sRecordName)
 인자값 = sTrCode – Tran 명
        sRecordName – 레코드 명
 반환값 = 레코드의 반복횟수

CommGetData 메서드 - 키움증권 서버로부터 TR 처리에 대한 이벤트가 발생했을 때 실제로 데이터를 가져올때 사용.

9) CommGetData
원형 BSTR CommGetData(…)
설명 이 함수는 지원하지 않을 것이므로 용도에 맞는 전용 함수를 사용할 것(비고참고)
입력값
반환값
비고
조회 정보 요청 - openApi.GetCommData(“OPT00001”, RQName, 0, “현재가”);
실시간정보 요청 - openApi.GetCommRealData(“000660”, 10);
체결정보 요청 - openApi.GetChejanData(9203);

OnReceiveTrData 이벤트 - TR 요청의 결과로 발생

 OnReceiveTrData
원형
    void OnReceiveTrData(LPCTSTR sScrNo, LPCTSTR sRQName, LPCTSTR sTrCode,
    LPCTSTR sRecordName, LPCTSTR sPreNext, LONG nDataLength, LPCTSTR sErrorCode,
    LPCTSTR sMessage, LPCTSTR sSplmMsg)
설명 서버통신 후 데이터를 받은 시점을 알려준다.
입력값
    sScrNo – 화면번호
    sRQName – 사용자구분 명
    sTrCode – Tran 명
    sRecordName – Record 명
    sPreNext – 연속조회 유무
    nDataLength – 1.0.0.1 버전 이후 사용하지 않음.
    sErrorCode – 1.0.0.1 버전 이후 사용하지 않음.
    sMessage – 1.0.0.1 버전 이후 사용하지 않음.
    sSplmMsg - 1.0.0.1 버전 이후 사용하지 않음.
반환값 없음
비고
    sRQName – CommRqData의 sRQName과 매핑되는 이름이다.
    sTrCode – CommRqData의 sTrCode과 매핑되는 이름이다.

 이벤트 -> 슬롯 연결 / _receive_tr_data 메서드가 호출 됐다는 것은.
 키움 서버로부터 'OnReceiveTrData' 이벤트가 발생했다는 것을 의미.
 따라서 _receive_tr_data 메서드 내에서 서버로부터 데이터를 받아오면 된다.

 _receive_tr_data 메서드 구현시 3가지 고려사항.
  1. 여러 종류의 TR을 요청해도 모두 _receive_tr_data 메서드 내에서 처리해야함.
     rqname 인자를 통해 요청한 TR을 구분한 뒤 TR에 따라 데이터를 가져오도록 작성.
     -> rqname 값이 opt10081_req일때 _opt10081 메서드를 호출.
        TR을 요청할 때 TR을 구분하기 위한 적당한 문자열을 사용.
        데이터를 받을 때는 해당 문자열과 같은지 확인함으로 올바른 데이터를 얻을 수 있다.
  2. 연속조회에 대한 처리.
     연속조회는 아직 데이터가 존재한다는 것을 의미.
     TR을 한 번 요청하면 900개의 데이터가 반환된다. / 10년치 데이터를 한 번의 TR 요청으로 받을 수 없다.
     이런 경우 TR을 또 요청해서 남은 데이터를 받아야 한다.
     키움 증권 서버는 OnReceiveTrData 이벤트가 발생할 때 PrevNext 인자값을 통해
     연속조회가 필요한 경우 PrevNext 값을 2로 리턴.
     따라서 PrevNext 값을 보고 2이면 데이터가 더 있다는 사실을 알 수 있고,
     이 경우 동일한 TR을 한 번 더 요청해서 남은 데이터를 가져와야 한다.

     아래 코드는 _receive_tr_data 메서드의 인자인 next의 값이 '2'일 때 self.remained_data라는 변수에 True를 저장.

  3. 이벤트 루프에 대한 처리.
     CommRqData를 호출할 때 이벤트 루프를 생성했다.
     이벤트 루프 덕분에 키움 증권 서버가 OnReceiveTrData 이벤트를 보낼 때까지 대기할 수 있었다.

     Kiwoom 클래스의 _receive_tr_data 메서드가 호출됐다는 것은
     정상적으로 대기 상태에서 머무르다가 서버로부터 발생한 OnReceiveTrData 이벤트를 받았음을 의미.
     따라서 _receive_tr_data 메서드에서 더는 필요하지 않은 이벤트 루프를 종료.

  opt10081_req에 대한 데이터는 opt10081 메서드에서 처리.
  이는 각 TR에 대한 데이터를 얻어가는 코드를 _receive_tr_data에 모두 구현하기 보다는 메서드로 따로 빼서 구현한 것.

키움은 초당 TR 요청 수를 제한 하고 있으니 참고해서 작성하자.
이 제한을 초과할 경우 일정 시간 이용 정지, 연속될시 더 긴 시간 정지 당한다.
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time

TR_REQ_TIME_INTERVAL = 0.2

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)

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

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        self.tr_event_loop =QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString", code, real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self,trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            date = self._comm_get_data(trcode, "", rqname, i, "일자")
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")
            print(date, open, high, low, close, volume)
        print(data_cnt)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    kiwoom.set_input_value("종목코드", "039490")
    kiwoom.set_input_value("기준일자", "20200316")
    kiwoom.set_input_value("수정주가구분", 1)
    kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")

    while kiwoom.remained_data == True:
        time.sleep(TR_REQ_TIME_INTERVAL)
        kiwoom.set_input_value("종목코드", "039490")
        kiwoom.set_input_value("기준일자", "20200316")
        kiwoom.set_input_value("수정주가구분", 1)
        kiwoom.comm_rq_data("opt10081_req", "opt10081", 2, "0101")
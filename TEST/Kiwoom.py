"""
SendOrder 메서드 - 주식 주문에 대한 정보를 서버로 전송
증권사 서버에 주문 요청을 했다고 즉시 체결되는 것이 아니므로 이벤트 루프를 사용해 대기.

주문이 체결되면 증권사 서버는 OnReceiveChejanData 이벤트 발생.
OnReceiveTrData 메서드 내에서 CommGetData 메서드를 호출해 데이터를 얻어왔듯이.
체결에 관해서는 OnReceiveChejanData 라는 메서드 내에서 GetChejanData 메서드를 호출해서 체결 잔고 데이터를 얻오면 된다.

SendOrder 메서드
원형
    LONG SendOrder( BSTR sRQName,
                    BSTR sScreenNo,
                    BSTR sAccNo,
                    LONG nOrderType,
                    BSTR sCode,
                    LONG nQty,
                    LONG nPrice,
                    BSTR sHogaGb,
                    BSTR sOrgOrderNo)
설명
    주식 주문을 서버로 전송한다.
입력값
    sRQName - 사용자 구분 요청 명
    sScreenNo - 화면번호[4]
    sAccNo - 계좌번호[10]
    nOrderType - 주문유형 (1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정
정)
    sCode, - 주식종목코드
    nQty – 주문수량
    nPrice – 주문단가
    sHogaGb - 거래구분
    sOrgOrderNo – 원주문번호
반환값
    에러코드 <4.에러코드표 참고>
비고
    sHogaGb – 00:지정가, 03:시장가, 05:조건부지정가, 06:최유리지정가, 07:최우선지정가, 10:지정가IOC,
            13:시장가IOC, 16:최유리IOC, 20:지정가FOK, 23:시장가FOK, 26:최유리FOK, 61:장전시간외종가,
            62:시간외단일가, 81:장후시간외종가
        ※ 시장가, 최유리지정가, 최우선지정가, 시장가IOC, 최유리IOC, 시장가FOK, 최유리FOK,
        장전시간외, 장후시간외 주문시 주문가격을 입력하지 않습니다.
ex)
지정가 매수 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 1, “000660”, 10,48500, “00”, “”);
시장가 매수 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 1, “000660”, 10, 0,“03”, “”);
매수 정정 - openApi.SendOrder(“RQ_1”,“0101”, “5015123410”, 5, “000660”, 10, 49500,“00”, “1”);
매수 취소 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 3, “000660”, 10, 0, “00”,“2”);

GetChejanData 메서드
    원형 BSTR GetChjanData(long nFid)
    설명 체결잔고 데이터를 반환한다.
    입력값 nFid – 체결잔고 아이템
    반환값 수신 데이터
    비고 Ex) 현재가출력 – openApi.GetChejanData(10);

주문체결 시점에 키움증권 서버가 발생시키는 OnReceiveChejanData 이벤트를 처리하는 메서드 구현.
OnReceiveChejanData 시그널과 슬롯을 연결

주문체결
FID 설명
9201 계좌번호
9203 주문번호
9205 관리자사번
9001 종목코드, 업종코드
912 주문업무분류(JJ:주식주문, FJ:선물옵션, JG:주식잔고, FG:선물옵션잔고)
913 주문상태(접수, 확인, 체결)
302 종목명
900 주문수량
901 주문가격
902 미체결수량
903 체결누계금액
904 원주문번호
905 주문구분(+현금내수,-현금매도…)
906 매매구분(보통,시장가…)
907 매도수구분 (1:매도,2:매수)
908 주문/체결시간(HHMMSSMS)
909 체결번호
910 체결가
911 체결량
10 현재가, 체결가, 실시간종가
27 (최우선)매도호가
28 (최우선)매수호가
914 단위체결가
915 단위체결량
938 당일매매 수수료
939 당일매매세금

GetLoginInfo 메서드 - OpenAPI+에서 계좌 정보 및로그인 사용자 정보를 얻어오는 메서드

원형
    BSTR GetLoginInfo(BSTR sTag)
설명
    로그인한 사용자 정보를 반환한다.
입력값
    BSTR sTag : 사용자 정보 구분 TAG값 (비고)
반환값
    TAG값에 따른 데이터 반환
비고
    BSTR sTag에 들어 갈 수 있는 값은 아래와 같음
    “ACCOUNT_CNT” – 전체 계좌 개수를 반환한다.
    "ACCNO" – 전체 계좌를 반환한다. 계좌별 구분은 ‘;’이다.
    “USER_ID” - 사용자 ID를 반환한다.
    “USER_NAME” – 사용자명을 반환한다.
    “KEY_BSECGB” – 키보드보안 해지여부. 0:정상, 1:해지
    “FIREW_SECGB” – 방화벽 설정 여부. 0:미설정, 1:설정, 2:해지
    Ex) openApi.GetLoginInfo(“ACCOUNT_CNT”);
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import pandas as pd
import sqlite3

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
        self.OnReceiveChejanData.connect(self._receive_chejan_data)

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
        code_name = self.dynamicCall("GetMasterCodeName(QString)",code)
        return code_name

    def get_connect_state(self):
        ret = self.dynamicCall("GetConnectState()")
        return ret

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("commRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code, real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
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
            low =  self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")

            self.ohlcv['date'].append(date)
            self.ohlcv['open'].append(int(open))
            self.ohlcv['high'].append(int(high))
            self.ohlcv['low'].append(int(low))
            self.ohlcv['close'].append(int(close))
            self.ohlcv['volume'].append(int(volume))

    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                         [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])

    def get_chejan_data(self, fid):
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        print(gubun)
        print(self.get_chejan_data(9203))
        print(self.get_chejan_data(302))
        print(self.get_chejan_data(900))
        print(self.get_chejan_data(901))

    def get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(QString)", tag)
        return ret


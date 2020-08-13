import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.error_code import *
from config.kiwoom_type import *
from config.log_class import *

class DB_Kiwoom(QAxWidget):
    def __init__(self):
        # kiwoom 클래스 시작
        super().__init__()

        self.logging = Logging(name="DB")

        self.logging.logger.info("DB_Kiwoom() class start")

        #### 초기 설정 함수
        self._create_kiwoom_instance()
        self._set_signal_slots()

        self.tr_request_time_interval = 0.7
        ###################

    def _create_kiwoom_instance(self):
        """
        키움 API 모듈 실행
        """
        self.logging.logger.info("Kiwoom api start")

        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")


    def _set_signal_slots(self):
        """
        이벤트 - 슬롯
        이벤트와 슬롯을 연결하는 메소드
        """
        self.logging.logger.info("signal_slots setting")

        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)

    def _event_connect(self, error_code):
        """
        키움 api 메소드인 CommConnect의 실행 후 OnEventConnect 이벤트가 발생
        err_code 인자값으로 로그인 성공 여부를 알 수 있다.

        OnEventConnect(통신 연결 상태 변경시 이벤트)가  서버 접속 관련 이벤트

        err_code가 0이면 로그인 성공, 음수면 실패

        :param error_code:
            config.error_code.py
        """
        error = errors(err_code=error_code)

        self.logging.logger.info("로그인 성공 여부 확인 | " + error[0] + " : " + error[1])

        self.login_event_loop.exit()

    def _get_repeat_cnt(self, trcode, rqname):
        """
        GetRepeatCnt 메소드 호출 (수신 받은 데이터의 반복 개수를 반환한다)
        """
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        """
        OnReceiveTrData(Tran 수신시 이벤트)가 서버통신 후 데이터를 받은 시점을 알려준다

        :param screen_no:화면번호
        :param rqname:사용자구분 명
            rqname – CommRqData의 rqname과 매핑되는 이름이다.
        :param trcode:Tran 명
            trcode – CommRqData의 trcode과 매핑되는 이름이다
        :param record_name:Record 명
        :param next:연속조회 유무
        """
        # self.logging.logger.info("OnReceiveTrData 이벤트와 연결된 슬롯 실행")

        if next == '2':
            self.remained_data = True
            self.logging.logger.info("TR Data 요청 | Rqname : " + rqname + ", TR Code : " + trcode + ", 연속조회 O")
        else:
            self.remained_data = False
            self.logging.logger.info("TR Data 요청 | Rqname : " + rqname + ", TR Code : " + trcode + ", 연속조회 X")

        if rqname == "주식일봉차트조회요청":
            self._opt10081(rqname=rqname, trcode=trcode)

        # OPT10023 opt10030 OPT10031 거래량 상위
        # opt10079 틱 차트 조회 KOA 돌려보기
        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opt10081(self, rqname, trcode):
        """
        :param rqname:주식일봉차트조회요청
        :param trcode:opt10081
        """
        cnt = self._get_repeat_cnt(trcode=trcode, rqname=rqname)

        self.stock_ohlcv = {'date': [], 'start': [], 'high': [], 'low': [], 'close': [], 'volume': []}

        for i in range(cnt):
            date = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="일자")
            start = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="시가")
            high = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="고가")
            low = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="저가")
            close = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="현재가")
            volume = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="거래량")

            self.stock_ohlcv['date'].append(date)
            self.stock_ohlcv['start'].append(start)
            self.stock_ohlcv['high'].append(high)
            self.stock_ohlcv['low'].append(low)
            self.stock_ohlcv['close'].append(close)
            self.stock_ohlcv['volume'].append(volume)

    def comm_connect(self):
        """
        CommConnect 메소드 호출 (로그인 윈도우를 실행한다)
        0 - 성공, 음수값은 실패
        """
        self.logging.logger.info("CommConnect 메소드 실행")

        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        """
        CommRqData 메소드 호출 (통신 데이터를 송신한다) / TR을 서버로 송신한다.

        :param rqname:사용자구분 명
        :param trcode:Tran명 입력
        :param next:0:조회, 2:연속
        :param screen_no:4자리의 화면번호

        반환값
            OP_ERR_SISE_OVERFLOW – 과도한 시세조회로 인한 통신불가
            OP_ERR_RQ_STRUCT_FAIL – 입력 구조체 생성 실패
            OP_ERR_RQ_STRING_FAIL – 요청전문 작성 실패
            OP_ERR_NONE – 정상처리
        """
        # self.logging.logger.info("CommRqData 메소드 실행")
        self.logging.logger.info("TR Data 송신 | Rqname : " + rqname + ", Screen Number : " + screen_no)

        self.dynamicCall("commRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def get_connect_state(self):
        """
        GetConnectState 메소드 호출 (통신 접속 상태를 반환한다.) / 현재접속상태를 반환한다.

        반환값
            접속상태

        비고
            0:미연결, 1:연결완료
        """
        # self.logging.logger.info("GetConnectState 메소드 실행")

        result = self.dynamicCall("GetConnectState()")
        return result

    def get_comm_data(self, trcode, rqname, index, name):
        """
        GetCommData 메소드 호출 (수신 데이터를 반환한다.)

        :param trcode:Tran 코드
        :param rqname:레코드명
        :param index:복수데이터 인덱스
        :param name:아이템명

        반환값
            수신 데이터
        """
        # self.logging.logger.info("GetCommData 메소드 실행")

        ret = self.dynamicCall("GetCommData(QString, QString, int, QString", trcode, rqname, index, name)
        return ret.strip()

    def get_login_info(self, s_Tag):
        """
        GetLoginInfo 메소드 호출 (로그인 정보를 반환한다.) / 로그인한 사용자 정보를 반환한다.

        :param s_Tag:사용자 정보 구분 TAG값

        반환값
            TAG값에 따른 데이터 변환

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
        # self.logging.logger.info("GetLoginInfo 메소드 실행")

        ret = self.dynamicCall("GetLoginInfo(QString)", s_Tag)

        self.logging.logger.info("사용자 정보 반환 | " + s_Tag + " : " + ret)

        return ret

    def get_master_code_name(self, code):
        """
        GetMasterCodeName 메소드 호출 (종목코드의 종목명을 반환한다.) / 종목코드의 한글명을 반환한다.

        :param code:종목코드

        반환값
            종목한글명
        """
        # self.logging.logger.info("GetMasterCodeName 메소드 실행")

        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)

        self.logging.logger.info("종목코드 -> 한글명 | 종목코드 : " + code + ", 종목명 : " + code_name)

        return code_name

    def get_code_list_by_market(self, market):
        """
        GetCodeListByMarket 메소드 호출 (장구분별 종목코드 리스트를 반환한다.) / 시장구분에 따른 종목코드를 반환한다.

        :param market:시장구분

        반환값
            종목코드 리스트, 종목간 구분은 ';'이다.

        비고
            sMarket – 0:장내, 3:ELW, 4:뮤추얼펀드, 5:신주인수권, 6:리츠,
                        8:ETF, 9:하이일드펀드, 10:코스닥, 30:K-OTC, 50:코넥스(KONEX)
        """
        code_list = []
        codes = self.dynamicCall("GetCodeListByMarket(QString)", market)
        print(codes)
        code_list = codes.split(';')
        print(code_list)
        return code_list[:-1]

    def set_input_value(self, id, value):
        """
        SetInputValue 메소드 호출 / Tran 입력 값을 서버통신 전에 입력한다.

        :param id:아이템명
        :param value:입력 값
        """
        # self.logging.logger.info("SetInputValue 메소드 실행")

        self.dynamicCall("SetInputValue(QString, QString)", id, value)



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     kiwoom = Kiwoom()
#     kiwoom.show()
#     kiwoom.comm_connect()
#     app.exec_()
#     app = None
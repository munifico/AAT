import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.error_code import *
from config.real_fid import *

class Kiwoom(QAxWidget):
    def __init__(self):
        # kiwoom 클래스 시작
        super().__init__()

        #### 초기 설정 함수
        self._create_kiwoom_instance()
        self._set_signal_slots()
        self.chejan_lists = []
        self.un_chejan_lists = []
        ###################

    def _create_kiwoom_instance(self):
        """
        키움 API 모듈 실행
        """
        print("kiwoom api start")
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")


    def _set_signal_slots(self):
        """
        이벤트 - 슬롯
        이벤트와 슬롯을 연결하는 메소드
        """
        print("signal_slots setting")
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)
        self.OnReceiveChejanData.connect(self._receive_chejan_data)
        self.OnReceiveRealData.connect(self._receive_real_data)

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

        print(error[0] + " : " + error[1])

        self.login_event_loop.exit()

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
        print("OnReceiveTrData 이벤트와 연결된 슬롯 실행")

        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "계좌평가잔고내역요청":
            self._opw00018(rqname=rqname, trcode=trcode)
        elif rqname == "예수금상세현황요청":
            self._opw00001(rqname=rqname, trcode=trcode)
        elif rqname == "관심종목정보요청":
            self._optkwfid(rqname=rqname, trcode=trcode)
        elif rqname == "전일대비등락률상위요청":
            self._opt10027(rqname=rqname, trcode=trcode)
        elif rqname == "거래량급증요청":
            self._opt10023(rqname=rqname, trcode=trcode)
        elif rqname == "당일거래량상위요청":
            self._opt10030(rqname=rqname, trcode=trcode)
        elif rqname == "전일거래량상위요청":
            self._opt10031(rqname=rqname, trcode=trcode)
        # OPT10023 opt10030 OPT10031 거래량 상위
        # opt10079 틱 차트 조회 KOA 돌려보기
        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opw00018(self, rqname, trcode):
        """
        :param rqname:계좌평가잔고내역요청
        :param trcode:opw00018
        """
        print("opw00018 TR Run")

        total_purchase_price = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=0, item_name="총매입금액")
        total_eval_price = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=0, item_name="총평가금액")
        total_eval_profit_loss_price = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=0, item_name="총평가손익금액")
        total_earning_rate = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=0, item_name="총수익률(%)")
        estimated_deposit = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=0, item_name="추정예탁자산")

        # self.reset_opw00018_output()

        self.opw00018_output['single'].append(Kiwoom.change_format(data=total_purchase_price))
        self.opw00018_output['single'].append(Kiwoom.change_format(data=total_eval_price))
        self.opw00018_output['single'].append(Kiwoom.change_format(data=total_eval_profit_loss_price))
        self.opw00018_output['single'].append(Kiwoom.change_format2(data=total_earning_rate))
        self.opw00018_output['single'].append(Kiwoom.change_format(data=estimated_deposit))

        rows = self._get_repeat_cnt(trcode=trcode, rqname=rqname)

        for i in range(rows):
            name = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=i, item_name="종목명")
            quantity = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=i, item_name="보유수량")
            purchase_price = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=i, item_name="매입가")
            current_price = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=i, item_name="현재가")
            eval_profit_loss_price = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=i, item_name="평가손익")
            earning_rate = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=i, item_name="수익률(%)")

            quantity = Kiwoom.change_format(data=quantity)
            purchase_price = Kiwoom.change_format(data=purchase_price)
            current_price = Kiwoom.change_format(data=current_price)
            eval_profit_loss_price = Kiwoom.change_format(data=eval_profit_loss_price)
            earning_rate = Kiwoom.change_format2(data=earning_rate)

            self.opw00018_output['multi'].append([name, quantity, purchase_price, current_price, eval_profit_loss_price, earning_rate])

            # print(self.opw00018_output['multi'])

    def _opw00001(self, rqname, trcode):
        """
        :param rqname:"예수금상세현황요청"
        :param trcode:"opw00001"
        """
        print("opw00001 TR Run")

        d2_deposit = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=0, item_name="d+2추정예수금")
        self.d2_deposit = Kiwoom.change_format(data=d2_deposit)

    def _optkwfid(self, rqname, trcode):
        """
        :param rqname:"관심종목정보요청"
        :param trcode:'OPTKWFID'
        """
        print("OPTKWFID TR Run")

        cnt = self._get_repeat_cnt(trcode=trcode, rqname=rqname)
        self.info_list = []

        for i in range(cnt):
            info = []

            code = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="종목코드")
            name = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="종목명")
            price = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="현재가")
            previous_day_price = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="전일대비")
            up_down_per = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="등락율")
            volume = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="거래량")
            yesterday_volume_per = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="전일거래량대비")

            info.append(code)
            info.append(name)
            info.append(price)
            info.append(previous_day_price)
            info.append(up_down_per)
            info.append(volume)
            info.append(yesterday_volume_per)

            # print("info = ", info)

            self.info_list.append(info)

    def _opt10027(self, rqname, trcode):
        """
        :param rqname:"전일대비등락률상위요청"
        :param trcode:"opt10027"
        """
        print("opt10027 TR Run")

        cnt = 100

        self.up_stock_list = []
        self.up_near_stock_list = []

        for i in range(cnt):
            up_stock = []
            up_near_stock = []

            code = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="종목코드")
            name = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="종목명")
            price = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="현재가")
            previous_day_price = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="전일대비")
            up_down_per = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="등락률")
            volume = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="현재거래량")
            buy_quantity = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="매수잔량")
            sell_quantity = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="매도잔량")

            up_down = up_down_per[1:]

            if float(up_down) > 28.0:
                up_stock.append(code)
                up_stock.append(name)
                up_stock.append(price)
                up_stock.append(previous_day_price)
                up_stock.append(up_down_per)
                up_stock.append(volume)
                up_stock.append(buy_quantity)
                up_stock.append(sell_quantity)

                self.up_stock_list.append(up_stock)
            else:
                up_near_stock.append(code)
                up_near_stock.append(name)
                up_near_stock.append(price)
                up_near_stock.append(previous_day_price)
                up_near_stock.append(up_down_per)
                up_near_stock.append(volume)
                up_near_stock.append(buy_quantity)
                up_near_stock.append(sell_quantity)

                self.up_near_stock_list.append(up_near_stock)

    def _opt10023(self, rqname, trcode):
        """
        :param rqname:"거래량급증요청"
        :param trcode:"OPT10023"
        """
        print("OPT10023 TR Run")

        cnt = self._get_repeat_cnt(trcode=trcode, rqname=rqname)

        self.surge_volume_list = []

        for i in range(cnt):
            surge_volume = []

            code = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="종목코드")
            name = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="종목명")
            price = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="현재가")
            previous_day_price = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="전일대비")
            up_down_per = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="전일대비")
            volume = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="현재거래량")
            rapid_increase_quantity = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="급증량")
            rapid_increase_per = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="급증률")

            surge_volume.append(code)
            surge_volume.append(name)
            surge_volume.append(price)
            surge_volume.append(previous_day_price)
            surge_volume.append(up_down_per)
            surge_volume.append(volume)
            surge_volume.append(rapid_increase_quantity)
            surge_volume.append(rapid_increase_per)

            self.surge_volume_list.append(surge_volume)

    def _opt10030(self, rqname, trcode):
        """
        :param rqname:"당일거래량상위요청"
        :param trcode:"opt10030"
        """
        print("opt10030 TR Run")

        cnt = self._get_repeat_cnt(trcode=trcode, rqname=rqname)

        self.today_volume_top = []

        for i in range(cnt):
            today_volume = []

            code = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="종목코드")
            name = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="종목명")
            price = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="현재가")
            up_down_per = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="등락률")
            volume = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="거래량")
            previous_day_price = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="전일비")
            transaction_spin = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="거래회전율")

            today_volume.append(code)
            today_volume.append(name)
            today_volume.append(price)
            today_volume.append(up_down_per)
            today_volume.append(volume)
            today_volume.append(previous_day_price)
            today_volume.append(transaction_spin)

            self.today_volume_top.append(today_volume)


    def _opt10031(self, rqname, trcode):
        """
        :param rqname:"전일거래량상위요청"
        :param trcode:"OPT10031"
        """
        print("OPT10031 TR Run")

        cnt = self._get_repeat_cnt(trcode=trcode, rqname=rqname)

        self.yesterday_volume_top = []

        for i in range(cnt):
            yesterday_volume = []

            code = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="종목코드")
            name = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="종목명")
            price = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="현재가")
            previous_day_price = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="전일대비")
            volume = self.get_comm_data(trcode, rqname=rqname, index=i, name="거래량")

            yesterday_volume.append(code)
            yesterday_volume.append(name)
            yesterday_volume.append(price)
            yesterday_volume.append(previous_day_price)
            yesterday_volume.append(volume)

            self.yesterday_volume_top.append(yesterday_volume)

    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        """
        OnReceiveChejanData(주문 접수/확인 수신시 이벤트)가 체결데이터를 받은 시점을 알려준다.
        :param gubun:체결구분
        :param item_cnt:아이템갯수
        :param fid_list:데이터리스트
        """
        print("OnReceiveChejanData와 연결된 슬롯 실행")

        sell_buy_num = {'1': "매도",
                        '2': "매수",
                        "": ""}

        order_num = self.get_chejan_data(9203)
        item_code = self.get_chejan_data(9001)
        state = self.get_chejan_data(913)
        name = self.get_chejan_data(302)
        name = name.strip()
        order_quantity = self.get_chejan_data(900)
        order_price = self.get_chejan_data(901)
        miss_quantity = self.get_chejan_data(902)
        sell_buy_gubun = self.get_chejan_data(907)
        origin_order_num = self.get_chejan_data(904)
        print("receive_chejan_data")
        print(sell_buy_num[sell_buy_gubun])
        if order_num == '':
            pass
        else:
            self.chejan_lists.append([order_num,origin_order_num, state, name, sell_buy_num[sell_buy_gubun], order_quantity, miss_quantity])
        # 미 체결 리스트는 나중에 추가
        # self.un_chejan_lists.append([order_num, item_code, order_quantity, miss_quantity, sell_buy_num[sell_buy_gubun]])

    def _receive_real_data(self, code, fid_type, data):
        print("real_data 이벤트 : ", fid_type)
        # print("real_data data : ", data)
        # print(type(data))

        if fid_type == "주식체결":
            self.real_data = []
            self.interest_data = []

            now_price = self.get_comm_real_data(code, 10)
            previous_day_price = self.get_comm_real_data(code, 11)
            up_down_per = self.get_comm_real_data(code, 12)
            first_sell_hoga = self.get_comm_real_data(code, 27)
            first_buy_hoga = self.get_comm_real_data(code, 28)
            trading_volume = self.get_comm_real_data(code, 13)
            trading_price = self.get_comm_real_data(code, 14)
            open = self.get_comm_real_data(code, 16)
            high = self.get_comm_real_data(code, 17)
            low = self.get_comm_real_data(code, 18)
            yester_trading_quantity_per = self.get_comm_real_data(code, 30)

            self.real_data.append(now_price)
            self.real_data.append(previous_day_price)
            self.real_data.append(up_down_per)
            self.real_data.append(first_sell_hoga)
            self.real_data.append(first_buy_hoga)
            self.real_data.append(trading_volume)
            self.real_data.append(trading_price)
            self.real_data.append(open)
            self.real_data.append(high)
            self.real_data.append(low)
            self.real_data.append(yester_trading_quantity_per)

            print(self.real_data)
################################################################################################

            print(code)
            name = self.get_master_code_name(code)
            price = self.get_comm_real_data(code, 10)
            previous_day_price = self.get_comm_real_data(code, 11)
            up_down_per = self.get_comm_real_data(code, 12)
            volume = self.get_comm_real_data(code, 13)
            yester_volume_per = self.get_comm_real_data(code, 30)

            self.interest_data.append(code)
            self.interest_data.append(name)
            self.interest_data.append(price)
            self.interest_data.append(previous_day_price)
            self.interest_data.append(up_down_per)
            self.interest_data.append(volume)
            self.interest_data.append(yester_volume_per)

            print(self.interest_data)

        elif fid_type == "주식호가잔량":
            self.real_hoga = []
            sub_ho = []
            sell_ho_list = []
            sell_ho_quantity_list = []
            buy_ho_list = []
            buy_ho_quantity_list = []

            ho_time = self.get_comm_real_data(code, 21)
            sell_total_quantity = self.get_comm_real_data(code, 121)
            buy_total_quantity = self.get_comm_real_data(code, 125)
            expect_che = self.get_comm_real_data(code, 23)
            expect_che_quantity = self.get_comm_real_data(code, 24)
            yester_close_expect_che = self.get_comm_real_data(code, 200)
            yester_close_expect_che_per = self.get_comm_real_data(code, 201)
            yester_close = int(expect_che) - int(yester_close_expect_che)
            up_max = yester_close + int(yester_close * 0.3)
            down_min = yester_close - int(yester_close * 0.3)
            total_trading_quantity = self.get_comm_real_data(code, 13)

            sub_ho.append(ho_time)
            sub_ho.append(sell_total_quantity)
            sub_ho.append(buy_total_quantity)
            sub_ho.append(expect_che)
            sub_ho.append(expect_che_quantity)
            sub_ho.append(yester_close_expect_che)
            sub_ho.append(yester_close_expect_che_per)
            sub_ho.append(str(up_max))
            sub_ho.append(str(down_min))
            sub_ho.append(total_trading_quantity)

            for i in range(41, 51):
                sell_ho_list.append(self.get_comm_real_data(code, i))

            for i in range(61, 71):
                sell_ho_quantity_list.append(self.get_comm_real_data(code, i))

            for i in range(51, 61):
                buy_ho_list.append(self.get_comm_real_data(code, i))

            for i in range(71, 81):
                buy_ho_quantity_list.append(self.get_comm_real_data(code, i))

            self.real_hoga.append(sub_ho)
            self.real_hoga.append(sell_ho_list)
            self.real_hoga.append(sell_ho_quantity_list)
            self.real_hoga.append(buy_ho_list)
            self.real_hoga.append(buy_ho_quantity_list)

            print(self.real_hoga)
            # sell_ho_1 = self.get_comm_real_data(code, 41)
            # sell_ho_2 = self.get_comm_real_data(code, 42)
            # sell_ho_3 = self.get_comm_real_data(code, 43)
            # sell_ho_4 = self.get_comm_real_data(code, 44)
            # sell_ho_5 = self.get_comm_real_data(code, 45)
            # sell_ho_6 = self.get_comm_real_data(code, 46)
            # sell_ho_7 = self.get_comm_real_data(code, 47)
            # sell_ho_8 = self.get_comm_real_data(code, 48)
            # sell_ho_9 = self.get_comm_real_data(code, 49)
            # sell_ho_10 = self.get_comm_real_data(code, 50)


            # sell_ho_quantity_1 = self.get_comm_real_data(code, 61)
            # sell_ho_quantity_2 = self.get_comm_real_data(code, 62)
            # sell_ho_quantity_3 = self.get_comm_real_data(code, 63)
            # sell_ho_quantity_4 = self.get_comm_real_data(code, 64)
            # sell_ho_quantity_5 = self.get_comm_real_data(code, 65)
            # sell_ho_quantity_6 = self.get_comm_real_data(code, 66)
            # sell_ho_quantity_7 = self.get_comm_real_data(code, 67)
            # sell_ho_quantity_8 = self.get_comm_real_data(code, 68)
            # sell_ho_quantity_9 = self.get_comm_real_data(code, 69)
            # sell_ho_quantity_10 = self.get_comm_real_data(code, 70)


            # buy_ho_1 = self.get_comm_real_data(code, 51)
            # buy_ho_2 = self.get_comm_real_data(code, 52)
            # buy_ho_3 = self.get_comm_real_data(code, 53)
            # buy_ho_4 = self.get_comm_real_data(code, 54)
            # buy_ho_5 = self.get_comm_real_data(code, 55)
            # buy_ho_6 = self.get_comm_real_data(code, 56)
            # buy_ho_7 = self.get_comm_real_data(code, 57)
            # buy_ho_8 = self.get_comm_real_data(code, 58)
            # buy_ho_9 = self.get_comm_real_data(code, 59)
            # buy_ho_10 = self.get_comm_real_data(code, 60)


            # buy_ho_quantity_1 = self.get_comm_real_data(code, 71)
            # buy_ho_quantity_2 = self.get_comm_real_data(code, 72)
            # buy_ho_quantity_3 = self.get_comm_real_data(code, 73)
            # buy_ho_quantity_4 = self.get_comm_real_data(code, 74)
            # buy_ho_quantity_5 = self.get_comm_real_data(code, 75)
            # buy_ho_quantity_6 = self.get_comm_real_data(code, 76)
            # buy_ho_quantity_7 = self.get_comm_real_data(code, 77)
            # buy_ho_quantity_8 = self.get_comm_real_data(code, 78)
            # buy_ho_quantity_9 = self.get_comm_real_data(code, 79)
            # buy_ho_quantity_10 = self.get_comm_real_data(code, 80)



    def _comm_get_data(self, code, real_type, rqname, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code, real_type, rqname, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def comm_connect(self):
        print("comm_connect")
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("commRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def comm_kw_rq_data(self, code_list, code_count, screen):
        print("comm_kw_rq_data")
        self.dynamicCall("CommKwRqData(QString, int, int, int, QString, QString)", code_list, 0, code_count, 0, "관심종목정보요청", screen)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def get_connect_state(self):
        result = self.dynamicCall("GetConnectState()")
        return result

    def get_comm_data(self, trcode, rqname, index, name):
        ret = self.dynamicCall("GetCommData(QString, QString, int, QString", trcode, rqname, index, name)
        return ret.strip()

    def get_comm_real_data(self, code, fid):
        ret = self.dynamicCall("GetCommRealData(QString, int)", code, fid)
        print("get_comm_real_data", ret)
        return ret

    def get_login_info(self, s_Tag):
        """
        BSTR sTag에 들어 갈 수 있는 값은 아래와 같음
        “ACCOUNT_CNT” – 전체 계좌 개수를 반환한다.
        "ACCNO" – 전체 계좌를 반환한다. 계좌별 구분은 ‘;’이다.
        “USER_ID” - 사용자 ID를 반환한다.
        “USER_NAME” – 사용자명을 반환한다.
        “KEY_BSECGB” – 키보드보안 해지여부. 0:정상, 1:해지
        “FIREW_SECGB” – 방화벽 설정 여부. 0:미설정, 1:설정, 2:해지
        Ex) openApi.GetLoginInfo(“ACCOUNT_CNT”);
        """
        ret = self.dynamicCall("GetLoginInfo(QString)", s_Tag)
        return ret

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def get_chejan_data(self, fid):
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        print(price)
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString",
                         [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])

    def reset_opw00018_output(self):
        self.opw00018_output = {'single': [], 'multi': []}

    # 초기에 보여줘야 하는 값 0으로 셋팅
    def reset_real_fid(self):
        self.real_data = ['0'] * 11
        self.real_hoga = [['0'] * 10 for i in range(5)]

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def set_real_reg(self, screen_no, code_list, fid_list, opt_type):
        # ret = self.dynamicCall("SetRealReg(QString, QString, QString, QString)", screen_no, code_list, fid_list, opt_type)
        # print("set_real_reg", ret)
        # return ret
        self.dynamicCall("SetRealReg(QString, QString, QString, QString)", screen_no, code_list, fid_list, opt_type)

    def set_real_remove(self, screen_no, code):
        print("set_real_remove")
        self.dynamicCall("SetRealRemove(QString, QString)", screen_no, code)

    @staticmethod
    def change_format(data):
        strip_data = data.lstrip('-0')

        if strip_data == '':
            strip_data = '0'

        try:
            format_data = format(int(strip_data), ',d')
        except:
            format_data = format(float(strip_data))

        if data.startswith('-'):
            format_data = '-' + format_data

        return format_data

    @staticmethod
    def change_format2(data):
        strip_data = data.lstrip('-0')

        if strip_data == '':
            strip_data = '0'

        if strip_data.startswith('.'):
            strip_data = '0' + strip_data

        if data.startswith('-'):
            strip_data = '-' + strip_data

        return strip_data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.show()
    kiwoom.comm_connect()
    app.exec_()
    app = None
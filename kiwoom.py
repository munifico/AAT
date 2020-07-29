import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.error_code import *
from config.kiwoom_type import *
from config.log_class import *

class Kiwoom(QAxWidget):
    def __init__(self):
        # kiwoom 클래스 시작
        super().__init__()

        self.logging = Logging()

        self.logging.logger.debug("Kiwoom() class start")

        #### 초기 설정 함수
        self._create_kiwoom_instance()
        self._set_signal_slots()

        self.chejan_lists = []
        self.un_chejan_lists = []

        # 체결 / 미체결 딕셔너리
        self.execution_list = []
        self.not_execution_list = []

        self.fid = RealType().REALTYPE
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
        elif rqname == "실시간미체결요청":
            self._opt10075(rqname=rqname, trcode=trcode)
        elif rqname == "실시간체결요청":
            self._opt10076(rqname=rqname, trcode=trcode)
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
            code = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=i, item_name="종목번호")
            name = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=i, item_name="종목명")
            quantity = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=i, item_name="보유수량")
            purchase_price = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=i, item_name="매입가")
            current_price = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=i, item_name="현재가")
            eval_profit_loss_price = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=i, item_name="평가손익")
            earning_rate = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=i, item_name="수익률(%)")

            code = code[1:]
            quantity = Kiwoom.change_format(data=quantity)
            purchase_price = Kiwoom.change_format(data=purchase_price)
            current_price = Kiwoom.change_format(data=current_price)
            eval_profit_loss_price = Kiwoom.change_format(data=eval_profit_loss_price)
            earning_rate = Kiwoom.change_format2(data=earning_rate)

            self.opw00018_output['multi'].append([code, name, quantity, purchase_price, current_price, eval_profit_loss_price, earning_rate])

            # print(self.opw00018_output['multi'])

    def _opw00001(self, rqname, trcode):
        """
        :param rqname:예수금상세현황요청
        :param trcode:opw00001
        """
        print("opw00001 TR Run")

        d2_deposit = self._comm_get_data(code=trcode, real_type="", rqname=rqname, index=0, item_name="d+2추정예수금")
        self.d2_deposit = Kiwoom.change_format(data=d2_deposit)

    def _optkwfid(self, rqname, trcode):
        """
        :param rqname:관심종목정보요청
        :param trcode:OPTKWFID
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
        :param rqname:전일대비등락률상위요청
        :param trcode:opt10027
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
        :param rqname:거래량급증요청
        :param trcode:OPT10023
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
        :param rqname:당일거래량상위요청
        :param trcode:opt10030
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
        :param rqname:전일거래량상위요청
        :param trcode:OPT10031
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

    def _opt10075(self, rqname, trcode):
        """
        :param rqname:실시간미체결요청
        :param trcode:opt10075
        """
        print("opt10075 TR Run")

        self.not_execution_list = []

        cnt = self._get_repeat_cnt(trcode=trcode, rqname=rqname)

        for i in range(cnt):
            not_execution_quantity = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="미체결수량")

            if not_execution_quantity != "0":
                order_num = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="주문번호")
                origin_order_num = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="원주문번호")
                order_status = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="주문상태")
                stock_name = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="종목명")
                order_type = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="주문구분")
                order_quantity = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="주문수량")
                execution_quantity = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="체결수량")

            # order_num = int(order_num)
            # origin_order_num = int(origin_order_num)
            # order_type = order_type.lstrip('+').lstrip('-')
            # order_quantity = int(order_quantity)
            # not_execution_quantity = int(not_execution_quantity)

                not_execution = [order_num, origin_order_num, order_status, stock_name,
                                order_type, order_quantity, not_execution_quantity, execution_quantity]

            # list_len = len(self.not_execution_list)

                self.not_execution_list.append(not_execution)
            # print(not_execution)

            # if list_len == 0:
            #     self.not_execution_list.append(not_execution)
            # else:
            #     for i in range(list_len):
            #         if order_num in self.not_execution_list[i][0]:
            #             del self.not_execution_list[i]
            #             self.not_execution_list.insert(i, not_execution)
            #         else:
            #             self.not_execution_list.append(not_execution)

    def _opt10076(self, rqname, trcode):
        """
        :param rqname:실시간체결요청
        :param trcode:opt10076
        """
        print("opt10076 TR Run")

        self.execution_list = []

        cnt = self._get_repeat_cnt(trcode=trcode, rqname=rqname)

        for i in range(cnt):
            not_execution_quantity = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="미체결수량")

            if not_execution_quantity == "0":
                order_num = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="주문번호")
                origin_order_num = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="원주문번호")
                order_status = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="주문상태")
                stock_name = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="종목명")
                order_type = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="주문구분")
                order_quantity = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="주문수량")
                execution_quantity = self.get_comm_data(trcode=trcode, rqname=rqname, index=i, name="체결수량")

            # order_num = int(order_num)
            # origin_order_num = int(origin_order_num)
            # order_type = order_type.lstrip('+').lstrip('-')
            # order_quantity = int(order_quantity)
            # execution_quantity = int(execution_quantity)

                execution = [order_num, origin_order_num, order_status, stock_name,
                                  order_type, order_quantity, execution_quantity, not_execution_quantity]

            # list_len = len(self.execution_list)

                self.execution_list.append(execution)
            # print(execution)
            # if list_len == 0:
            #     self.execution_list.append(execution)
            # elif list_len != 0:
            #     for i in range(list_len):
            #         if order_num in self.execution_list[i][0]:
            #             del self.execution_list[i]
            #             self.execution_list.insert(i, execution_list)
            #         else:
            #             self.execution_list.append(execution_list)

            # if order_num in self.execution_dict:
            #     pass
            # else:
            #     self.execution_dict[order_num] = {}
            #
            # self.execution_list[order_num].update({'주문번호': order_num})
            # self.execution_list[order_num].update({'원주문번호': origin_order_num})
            # self.execution_list[order_num].update({'주문상태': order_status})
            # self.execution_list[order_num].update({'종목명': stock_name})
            # self.execution_list[order_num].update({'주문구분': order_type})
            # self.execution_list[order_num].update({'주문수량': order_quantity})
            # self.execution_list[order_num].update({'체결수량': execution_quantity})

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

        order_num = self.get_chejan_data(fid=self.fid['주문체결']['주문번호'])
        item_code = self.get_chejan_data(fid=self.fid['주문체결']['종목코드'])
        status = self.get_chejan_data(fid=self.fid['주문체결']['주문상태'])
        name = self.get_chejan_data(fid=self.fid['주문체결']['종목명'])
        name = name.strip()
        order_quantity = self.get_chejan_data(fid=self.fid['주문체결']['주문수량'])
        order_price = self.get_chejan_data(fid=self.fid['주문체결']['주문가격'])
        miss_quantity = self.get_chejan_data(fid=self.fid['주문체결']['미체결수량'])
        sell_buy_gubun = self.get_chejan_data(fid=self.fid['주문체결']['매도수구분'])
        origin_order_num = self.get_chejan_data(fid=self.fid['주문체결']['원주문번호'])
        # print("receive_chejan_data")
        # print(sell_buy_num[sell_buy_gubun])
        if order_num == '':
            pass
        else:
            self.chejan_lists.append(
                [order_num, origin_order_num, status, name, sell_buy_num[sell_buy_gubun], order_quantity, miss_quantity])

        # order_num = self.get_chejan_data(9203)
        # item_code = self.get_chejan_data(9001)
        # state = self.get_chejan_data(913)
        # name = self.get_chejan_data(302)
        # name = name.strip()
        # order_quantity = self.get_chejan_data(900)
        # order_price = self.get_chejan_data(901)
        # miss_quantity = self.get_chejan_data(902)
        # sell_buy_gubun = self.get_chejan_data(907)
        # origin_order_num = self.get_chejan_data(904)
        # print("receive_chejan_data")
        # print(sell_buy_num[sell_buy_gubun])
        # if order_num == '':
        #     pass
        # else:
        #     self.chejan_lists.append([order_num,origin_order_num, state, name, sell_buy_num[sell_buy_gubun], order_quantity, miss_quantity])
        # # 미 체결 리스트는 나중에 추가
        # # self.un_chejan_lists.append([order_num, item_code, order_quantity, miss_quantity, sell_buy_num[sell_buy_gubun]])

    def _receive_real_data(self, code, fid_type, data):
        """
        OnReceiveRealData(실시간 시세 이벤트)가 실시간데이터를 받은 시점을 알려준다.

        :param code:종목코드
        :param fid_type:리얼타입
        :param data:실시간 데이터전문
        """
        print("OnReceiveRealData와 연결된 슬롯 실행")
        print("real_data 이벤트 : ", fid_type)
        # print("real_data data : ", data)
        # print(type(data))

        if fid_type == "주식체결":
            self.real_data = []
            self.interest_data = []

            now_price = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['현재가'])
            previous_day_price = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['전일대비'])
            up_down_per = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['등락율'])
            first_sell_hoga = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['(최우선)매도호가'])
            first_buy_hoga = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['(최우선)매수호가'])
            trading_volume = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['누적거래량'])
            trading_price = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['누적거래대금'])
            open = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['시가'])
            high = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['고가'])
            low = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['저가'])
            yester_trading_quantity_per = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['전일거래량대비'])

            # now_price = self.get_comm_real_data(code, 10)
            # previous_day_price = self.get_comm_real_data(code, 11)
            # up_down_per = self.get_comm_real_data(code, 12)
            # first_sell_hoga = self.get_comm_real_data(code, 27)
            # first_buy_hoga = self.get_comm_real_data(code, 28)
            # trading_volume = self.get_comm_real_data(code, 13)
            # trading_price = self.get_comm_real_data(code, 14)
            # open = self.get_comm_real_data(code, 16)
            # high = self.get_comm_real_data(code, 17)
            # low = self.get_comm_real_data(code, 18)
            # yester_trading_quantity_per = self.get_comm_real_data(code, 30)

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
            #
            # print(self.real_data)
################################################################################################
            #
            # print(code)
            name = self.get_master_code_name(code=code)
            price = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['현재가'])
            previous_day_price = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['전일대비'])
            up_down_per = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['등락율'])
            volume = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['누적거래량'])
            yester_volume_per = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['전일거래량대비'])

            # name = self.get_master_code_name(code=code)
            # price = self.get_comm_real_data(code=code, 10)
            # previous_day_price = self.get_comm_real_data(code=code, 11)
            # up_down_per = self.get_comm_real_data(code=code, 12)
            # volume = self.get_comm_real_data(code=code, 13)
            # yester_volume_per = self.get_comm_real_data(code=code, 30)

            self.interest_data.append(code)
            self.interest_data.append(name)
            self.interest_data.append(price)
            self.interest_data.append(previous_day_price)
            self.interest_data.append(up_down_per)
            self.interest_data.append(volume)
            self.interest_data.append(yester_volume_per)

            # print(self.interest_data)

        elif fid_type == "주식호가잔량":
            self.real_hoga = []
            sub_ho = []
            sell_ho_list = []
            sell_ho_quantity_list = []
            buy_ho_list = []
            buy_ho_quantity_list = []

            ho_time = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['호가시간'])
            sell_total_quantity = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['매도호가총잔량'])
            buy_total_quantity = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['매수호가총잔량'])
            expect_che = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['예상체결가1'])
            expect_che_quantity = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['예상체결수량'])
            yester_close_expect_che = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['예상체결가전일대비'])
            yester_close_expect_che_per = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['예상체결가전일대비등락율'])
            yester_close = int(expect_che) - int(yester_close_expect_che)
            up_max = int(yester_close) + int(yester_close * 0.3)
            down_min = int(yester_close) - int(yester_close * 0.3)
            total_trading_quantity = self.get_comm_real_data(code=code, fid=self.fid[fid_type]['누적거래량'])

            # ho_time = self.get_comm_real_data(code, 21)
            # sell_total_quantity = self.get_comm_real_data(code, 121)
            # buy_total_quantity = self.get_comm_real_data(code, 125)
            # expect_che = self.get_comm_real_data(code, 23)
            # expect_che_quantity = self.get_comm_real_data(code, 24)
            # yester_close_expect_che = self.get_comm_real_data(code, 200)
            # yester_close_expect_che_per = self.get_comm_real_data(code, 201)
            # yester_close = int(expect_che) - int(yester_close_expect_che)
            # up_max = yester_close + int(yester_close * 0.3)
            # down_min = yester_close - int(yester_close * 0.3)
            # total_trading_quantity = self.get_comm_real_data(code, 13)

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
                sell_ho_list.append(self.get_comm_real_data(code=code, fid=i))

            for i in range(61, 71):
                sell_ho_quantity_list.append(self.get_comm_real_data(code=code, fid=i))

            for i in range(51, 61):
                buy_ho_list.append(self.get_comm_real_data(code=code, fid=i))

            for i in range(71, 81):
                buy_ho_quantity_list.append(self.get_comm_real_data(code=code, fid=i))

            self.real_hoga.append(sub_ho)
            self.real_hoga.append(sell_ho_list)
            self.real_hoga.append(sell_ho_quantity_list)
            self.real_hoga.append(buy_ho_list)
            self.real_hoga.append(buy_ho_quantity_list)
            #
            # print(self.real_hoga)
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
        """
        print("삭제 예정인 조회 메소드")
        """
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code, real_type, rqname, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        """
        GetRepeatCnt 메소드 호출 (수신 받은 데이터의 반복 개수를 반환한다)
        """

        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def comm_connect(self):
        """
        CommConnect 메소드 호출 (로그인 윈도우를 실행한다)
        0 - 성공, 음수값은 실패
        """
        print("CommConnect 메소드 실행")

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
        print("CommRqData 메소드 실행")

        self.dynamicCall("commRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def comm_kw_rq_data(self, code_list, code_count, screen, next=0, type=0, rqname="관심종목정보요청"):
        """
        CommKwRqData 메소드 호출 (관심종목을 조회 한다.) / 복수종목조회 Tran을 서버로 송신한다.

        :param code_list:종목리스트
        :param code_count:종목개수
        :param screen:화면번호[4]
        :param next:연속조회요청
        :param type:조회구분
        :param rqname:사용자구분 명

        반환값
            OP_ERR_RQ_STRING – 요청 전문 작성 실패
            OP_ERR_NONE - 정상처리

        비고
            sArrCode – 종목간 구분은 ‘;’이다.
        """
        print("CommKwRqData 메소드 실행")

        self.dynamicCall("CommKwRqData(QString, int, int, int, QString, QString)", code_list, next, code_count, type, rqname, screen)
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
        print("GetConnectState 메소드 실행")

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
        print("GetCommData 메소드 실행")

        ret = self.dynamicCall("GetCommData(QString, QString, int, QString", trcode, rqname, index, name)
        return ret.strip()

    def get_comm_real_data(self, code, fid):
        """
        GetCommRealData 메소드 호출 (실시간 데이터를 반환한다.) / 실시간 시세 데이터를 반환한다

        :param code:종목코드
        :param fid:실시간 아이템

        반환값
            수신 데이터
        """
        print("GetCommRealData 메소드 실행")

        ret = self.dynamicCall("GetCommRealData(QString, int)", code, fid)
        return ret

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
        print("GetLoginInfo 메소드 실행")

        ret = self.dynamicCall("GetLoginInfo(QString)", s_Tag)
        return ret

    def get_master_code_name(self, code):
        """
        GetMasterCodeName 메소드 호출 (종목코드의 종목명을 반환한다.) / 종목코드의 한글명을 반환한다.

        :param code:종목코드

        반환값
            종목한글명
        """
        print("GetMasterCodeName 메소드 실행")

        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def get_master_construction(self, code):
        """
        GetMasterConstruction 메소드 호출 (종목코드의 감리구분을 반환한다.)

        :param code:종목코드

        반환값
            감리구분

        비고
            감리구분 – 정상, 투자주의, 투자경고, 투자위험, 투자주의환기종목
        """
        print("GetMasterConstruction 메소드 실행")

        construction = self.dynamicCall("GetMasterConstruction(QString)", code)
        return construction

    def get_master_stock_state(self, code):
        """
        GetMasterStockState 메소드 호출 (종목코드의 종목상태를 반환한다.)

        :param code:종목코드

        반환값
            종목상태

        비고
            종목상태 – 정상, 증거금100%, 거래정지, 관리종목, 감리종목, 투자유의종목, 담보대출, 액면분할, 신용가능
        """
        print("GetMasterStockState 메소드 실행")

        stock_state = self.dynamicCall("GetMasterStockState(QString)", code)
        return stock_state

    def get_chejan_data(self, fid):
        """
        GetChejanData 메소드 호출 (체결잔고 데이터를 반환한다)

        :param fid: 체결잔고 아이템

        반환값
            수신 데이터
        """
        print("GetChejanData 메소드 실행")

        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        """
        SendOrder 메소드 호출 (주식주문 Tran을 송신한다.) / 주식 주문을 서버로 전송한다

        :param rqname:사용자 구분 요청 명
        :param screen_no:화면번호[4]
        :param acc_no:계좌번호[10]
        :param order_type:주문유형 (1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정)
        :param code:주식종목코드
        :param quantity:주문수량
        :param price:주문단가
        :param hoga:거래구분
        :param order_no:원주문번호

        반환값
            에러코드 (/config/error_code.py)

        비고
            sHogaGb – 00:지정가, 03:시장가, 05:조건부지정가, 06:최유리지정가, 07:최우선지정가, 10:지정가IOC, 13:시장가IOC,
                    16:최유리IOC, 20:지정가FOK, 23:시장가FOK, 26:최유리FOK, 61:장전시간외종가, 62:시간외단일가, 81:장후시간외종가
                    ※ 시장가, 최유리지정가, 최우선지정가, 시장가IOC, 최유리IOC, 시장가FOK, 최유리FOK, 장전시간외, 장후시간외 주문시 주문가격을 입력하지 않습니다.
        """
        print("SendOrder 메소드 실행")

        # print(price)
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString",
                         [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])

    def reset_opw00018_output(self):
        self.opw00018_output = {'single': [], 'multi': []}

    # 초기에 보여줘야 하는 값 0으로 셋팅
    def reset_real_fid(self):
        self.real_data = ['0'] * 11
        self.real_hoga = [['0'] * 10 for i in range(5)]

    def set_input_value(self, id, value):
        """
        SetInputValue 메소드 호출 / Tran 입력 값을 서버통신 전에 입력한다.

        :param id:아이템명
        :param value:입력 값
        """
        print("SetInputValue 메소드 실행")

        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def set_real_reg(self, screen_no, code_list, fid_list, opt_type):
        """
        SetRealReg 메소드 호출 (실시간 등록을 한다.)

        :param screen_no:실시간 등록할 화면 번호
        :param code_list:실시간 등록할 종목코드(복수종목가능 – “종목1;종목2;종목3;….”)
        :param fid_list:실시간 등록할 FID(“FID1;FID2;FID3;…..”)
        :param opt_type:“0”, “1” 타입

        반환값
            통신결과

        비고
            strRealType이 “0” 으로 하면 같은화면에서 다른종목 코드로 실시간 등록을 하게 되면
                마지막에 사용한 종목코드만 실시간 등록이 되고 기존에 있던 종목은 실시간이 자동 해지됨.
            “1”로 하면 같은화면에서 다른 종목들을 추가하게 되면 기존에 등록한 종목도 함께 실시간 시세를 받을 수 있음.
        """
        print("SetRealReg 메소드 실행")

        # ret = self.dynamicCall("SetRealReg(QString, QString, QString, QString)", screen_no, code_list, fid_list, opt_type)
        # print("set_real_reg", ret)
        # return ret
        self.dynamicCall("SetRealReg(QString, QString, QString, QString)", screen_no, code_list, fid_list, opt_type)

    def set_real_remove(self, screen_no, code):
        """
        SetRealRemove 메소드 호출 (종목별 실시간 해제 (SetRealReg로 등록한 종목만 해제 가능)) /

        :param screen_no: 실시간 해제할 화면 번호
        :param code:실시간 해제할 종목.

        반환값
            통신결과
        """
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
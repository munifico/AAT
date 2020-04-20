import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()
        self.chejan_lists = []
        self.un_chejan_lists = []

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        print("create kiwoom")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)
        self.OnReceiveChejanData.connect(self._receive_chejan_data)
        self.OnReceiveRealData.connect(self._receive_real_data)
        print("signal_slots")

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connect")
        else:
            print("disconnect")

        self.login_event_loop.exit()

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opw00018_req":
            self._opw00018(rqname, trcode)
        elif rqname == "opw00001_req":
            self._opw00001(rqname, trcode)
        elif rqname == "":
            pass

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opw00018(self, rqname, trcode):
        total_purchase_price = self._comm_get_data(trcode, "", rqname, 0, "총매입금액")
        total_eval_price = self._comm_get_data(trcode, "", rqname, 0, "총평가금액")
        total_eval_profit_loss_price = self._comm_get_data(trcode, "", rqname, 0, "총평가손익금액")
        total_earning_rate = self._comm_get_data(trcode, "", rqname, 0, "총수익률(%)")
        estimated_deposit = self._comm_get_data(trcode, "", rqname, 0, "추정예탁자산")

        # self.reset_opw00018_output()

        self.opw00018_output['single'].append(Kiwoom.change_format(total_purchase_price))
        self.opw00018_output['single'].append(Kiwoom.change_format(total_eval_price))
        self.opw00018_output['single'].append(Kiwoom.change_format(total_eval_profit_loss_price))
        self.opw00018_output['single'].append(Kiwoom.change_format2(total_earning_rate))
        self.opw00018_output['single'].append(Kiwoom.change_format(estimated_deposit))

        rows = self._get_repeat_cnt(trcode, rqname)

        for i in range(rows):
            name = self._comm_get_data(trcode, "", rqname, i, "종목명")
            quantity = self._comm_get_data(trcode, "", rqname, i, "보유수량")
            purchase_price = self._comm_get_data(trcode, "", rqname, i, "매입가")
            current_price = self._comm_get_data(trcode, "", rqname, i, "현재가")
            eval_profit_loss_price = self._comm_get_data(trcode, "", rqname, i, "평가손익")
            earning_rate = self._comm_get_data(trcode, "", rqname, i, "수익률(%)")

            quantity = Kiwoom.change_format(quantity)
            purchase_price = Kiwoom.change_format(purchase_price)
            current_price = Kiwoom.change_format(current_price)
            eval_profit_loss_price = Kiwoom.change_format(eval_profit_loss_price)
            earning_rate = Kiwoom.change_format2(earning_rate)

            self.opw00018_output['multi'].append([name, quantity, purchase_price, current_price, eval_profit_loss_price, earning_rate])

    def _opw00001(self, rqname, trcode):
        d2_deposit = self._comm_get_data(trcode, "", rqname, 0, "d+2추정예수금")
        self.d2_deposit = Kiwoom.change_format(d2_deposit)

    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        '''
        FID        설명
        9201        계좌번호
        9203        주문번호
        9205        관리자사번
        9001        종목코드, 업종코드
        912        주문업무분류(JJ: 주식주문, FJ: 선물옵션, JG: 주식잔고, FG: 선물옵션잔고)
        913        주문상태(접수, 확인, 체결)
        302        종목명
        900        주문수량
        901        주문가격
        902        미체결수량
        903        체결누계금액
        904        원주문번호
        905        주문구분(+현금내수, -현금매도…)
        906        매매구분(보통, 시장가…)
        907        매도수구분(1: 매도, 2: 매수)
        908        주문 / 체결시간(HHMMSSMS)
        909        체결번호
        910        체결가
        911        체결량
        10        현재가, 체결가, 실시간종가
        27(최우선)        매도호가
        28(최우선)        매수호가
        914        단위체결가
        915        단위체결량
        938        당일매매 수수료
        939        당일매매세금
        '''
        sell_buy_num = {'1': "매도",
                        '2': "매수",
                        "" : ""}

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



    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code, real_type, field_name, index, item_name)
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

    def comm_kw_rq_data(self, code_list, next, code_count, type_flag, rqname, screen):
        pass

    def get_connect_state(self):
        result = self.dynamicCall("GetConnectState()")
        return result

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
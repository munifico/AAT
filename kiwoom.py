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

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

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

    def get_connect_state(self):
        result = self.dynamicCall("GetConnectState()")
        return result

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

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)


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
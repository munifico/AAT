from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from kiwoom import *
import time

form_class = uic.loadUiType("trading.ui")[0]

class Trading(QMainWindow, form_class):
    def __init__(self, parent, kiwoom):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)

        """
        중복 로그인 문제가 발생할 수도 있음.
        따라서 main에서 접속한 comm 정보를 받아와야함
        """
        # if connect_state == 1:
        #     self.kiwoom.comm_connect()
        # elif connect_state == 0:
        #     QCoreApplication.instance().quit()
        # print(connect_state)
        """
        해결
        """
        self.kiwoom = kiwoom
        # if connect_state == 1:
        #     self.kiwoom = kiwoom
        # elif connect_state == 0:
        #     """
        #     이 윈도우만 꺼지게 해야함.3
        #     """
        #     # qApp.quit()
        #     self.kiwoom = kiwoom
        #     # QCoreApplication.instance().quit()
        #     # QApplication(sys.argv).quit()
        #     self.close()
        if self.kiwoom.get_login_info("ACCOUNT_CNT") != '':
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.checkBox.setEnabled(True)
            self.checkBox_2.setEnabled(False)

            account_num = int(self.kiwoom.get_login_info("ACCOUNT_CNT"))
            accounts = self.kiwoom.get_login_info("ACCNO")
            accounts_list = accounts.split(';')[0:account_num]
            self.comboBox.addItems(accounts_list)

            self.lineEdit.textChanged.connect(self.code_changed)
            self.lineEdit_4.textChanged.connect(self.code_changed_hoga)

            self.pushButton.clicked.connect(self.send_order)
            self.pushButton_2.clicked.connect(self.check_balance)
            self.pushButton_3.clicked.connect(lambda:self.set_stacked_widget(num=0))
            self.pushButton_4.clicked.connect(lambda:self.set_stacked_widget(num=1))
            self.pushButton_5.clicked.connect(lambda:self.set_stacked_widget(num=2))
            self.pushButton_6.clicked.connect(lambda:self.set_stacked_widget(num=3))
            self.pushButton_7.clicked.connect(lambda:self.set_stacked_widget(num=4))
            self.pushButton_8.clicked.connect(lambda:self.set_stacked_widget(num=5))
            self.pushButton_9.clicked.connect(self.hoga)

            self.comboBox_3.activated.connect(self.type_changed)
            self.comboBox_2.activated.connect(self.type_order)

            self.timer = QTimer(self)
            self.timer.start(1000*10)
            self.timer.timeout.connect(self.stacked_0_timeout)

            self.timer = QTimer(self)
            self.timer.start(1000*1)
            self.timer.timeout.connect(self.stacked_1_timeout)
        else:
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.checkBox.setEnabled(False)

    def hoga(self):
        """
        8.1 주식시세
            FID 설명
            10 현재가, 체결가, 실시간종가
            11 전일 대비
            12 등락율
            27 (최우선)매도호가
            28 (최우선)매수호가
            13 누적거래량, 누적첵ㄹ량
            14 누적거래대금
            16 시가
            17 고가
            18 저가
            26 전일거래량 대비(계약,주)
            30 전일거래량 대비(비율)
            31 거래회전율
            32 거래비용
            311 시가총액(억)
        8.4 주식호가잔량
            FID 설명
            21 호가시간
            41 매도호가1
            61 매도호가 수량1
            81 매도호가 직전대비1
            51 매수호가1
            71 매수호가 수량1
            91 매수호가 직전대비1
            42 매도호가1
            62 매도호가 수량2
            82 매도호가 직전대비2
            52 매수호가2
            72 매수호가 수량2
            92 매수호가 직전대비2
            43 매도호가3
            63 매도호가 수량3
            83 매도호가 직전대비3
            53 매수호가3
            73 매수호가 수량3
            93 매수호가 직전대비3
            44 매도호가4
            64 매도호가 수량4
            84 매도호가 직전대비4
            54 매수호가4
            74 매수호가 수량4
            94 매수호가 직전대비4
            45 매도호가5
            65 매도호가 수량5
            85 매도호가 직전대비5
            55 매수호가5
            75 매수호가 수량5
            95 매수호가 직전대비5
            46 매도호가6
            66 매도호가 수량6
            86 매도호가 직전대비6
            56 매수호가6
            76 매수호가 수량6
            96 매수호가 직전대비6
            47 매도호가7
            67 매도호가 수량7
            87 매도호가 직전대비7
            57 매수호가7
            77 매수호가 수량7
            97 매수호가 직전대비7
            48 매도호가8
            68 매도호가 수량8
            88 매도호가 직전대비8
            58 매수호가8
            78 매수호가 수량8
            98 매수호가 직전대비8
            49 매도호가9
            69 매도호가 수량9
            89 매도호가 직전대비9
            59 매수호가9
            79 매수호가 수량9
            99 매수호가 직전대비9
            50 매도호가10
            70 매도호가 수량10
            90 매도호가 직전대비10
            60 매수호가10
            80 매수호가 수량10
            100 매수호가 직전대비10
            121 매도호가 총잔량
            122 매도호가 총잔량 직전대비
            125 매수호가 총잔량
            126 매수호가 총잔량 직전대비
            23 예상체결가
            24 예상체결 수량
            128 순매수잔량(총매수잔량-총매도잔량)
            129 매수비율
            138 순매도잔량(총매도잔량-총매수잔량)
            139 매도비율
            200 예상체결가 전일종가 대비
            201 예상체결가 전일종가 대비 등락율
            238 예상체결가 전일종가 대비기호
            291 예상체결가
            292 예상체결량
            293 예상체결가 전일대비기호
            294 예상체결가 전일대비
            295 예상체결가 전일대비등락율
            621 LP매도호가 수량1
            631 LP매수호가 수량1
            622 LP매도호가 수량2
            632 LP매수호가 수량2
            623 LP매도호가 수량3
            633 LP매수호가 수량3
            624 LP매도호가 수량4
            634 LP매수호가 수량4
            625 LP매도호가 수량5
            635 LP매수호가 수량5
            626 LP매도호가 수량6
            636 LP매수호가 수량6
            627 LP매도호가 수량7
            637 LP매수호가 수량7
            628 LP매도호가 수량8
            638 LP매수호가 수량8
            629 LP매도호가 수량9
            639 LP매수호가 수량9
            630 LP매도호가 수량10
            640 LP매수호가 수량10
            13 누적거래량, 누적체결량
            299 전일거래량대비예상체결률
            215 장운영구분
            216 투자자별 ticker
        """
        self.checkBox_2.setEnabled(True)

        code = self.lineEdit_4.text()
        # fid_list = "41;51;42;52;27;28;10;11;12;15;13;14;16;17;18"
        fid_list = "10;11;12;27;28;13;14;16;17;18"
        type = 0
        # 10 현재가, 체결가, 실시간종가
        #     11 전일 대비
        #     12 등락율
        #     27 (최우선)매도호가
        #     28 (최우선)매수호가
        #     13 누적거래량, 누적첵ㄹ량
        #     14 누적거래대금
        #     16 시가
        #     17 고가
        #     18 저가
        #     26 전일거래량 대비(계약,주)
        #     30 전일거래량 대비(비율)
        #     31 거래회전율
        #     32 거래비용
        #     311 시가총액(억)

        # default_info = self.kiwoom.set_real_reg(6000, code, fid_list, type)
        # print("default_info :", default_info)
        self.kiwoom.reset_real_fid()

        self.kiwoom.set_real_reg(6000, code, fid_list, type)

        self.lineEdit_6.setText(self.kiwoom.real_data[0])
        self.label_41.setText(self.kiwoom.real_data[0])
        self.label_42.setText(self.kiwoom.real_data[1])
        self.label_43.setText(self.kiwoom.real_data[2])
        self.label_44.setText(self.kiwoom.real_data[5])
        self.label_45.setText(self.kiwoom.real_data[6])
        self.label_51.setText(self.kiwoom.real_data[7])
        self.label_52.setText(self.kiwoom.real_data[8])
        self.label_53.setText(self.kiwoom.real_data[9])
        self.label_54.setText(self.kiwoom.real_data[3])
        self.label_55.setText(self.kiwoom.real_data[4])

    def set_stacked_widget(self, num):
        if num == 0:
            self.stackedWidget.setCurrentIndex(0)
        elif num == 1:
            self.stackedWidget.setCurrentIndex(1)
        elif num == 2:
            self.stackedWidget.setCurrentIndex(2)
        elif num == 3:
            self.stackedWidget.setCurrentIndex(3)
        elif num == 4:
            self.stackedWidget.setCurrentIndex(4)
        elif num == 5:
            self.stackedWidget.setCurrentIndex(5)
        self.lcdNumber.display(num)

    def type_changed(self, index):
        print(index)
        if index == 1:
            self.spinBox_2.setValue(0)

    def type_order(self, index):
        if index == 0 or index == 1:
            self.lineEdit_3.setText('')

    def code_changed(self):
        code = self.lineEdit.text()
        name = self.kiwoom.get_master_code_name(code)
        self.lineEdit_2.setText(name)

    def code_changed_hoga(self):
        code = self.lineEdit_4.text()
        name = self.kiwoom.get_master_code_name(code=code)
        self.lineEdit_5.setText(name)
        self.lineEdit.setText(code)

    def send_order(self):
        """
        매수 정정, 매도 정정은 거래 내역 만들고 추가
        """
        order_type_lookup = {'신규매수': 1, '신규매도': 2, '매수취소': 3, '매도취소':4}
        hoga_lookup = {'지정가': '00', '시장가': '03'}

        account = self.comboBox.currentText()
        order_type = self.comboBox_2.currentText()
        code = self.lineEdit.text()
        hoga = self.comboBox_3.currentText()
        num = self.spinBox.value()
        price = self.spinBox_2.value()
        order_num = self.lineEdit_3.text()

        self.kiwoom.send_order("send_order_req", "0101", account, order_type_lookup[order_type], code, num, price, hoga_lookup[hoga], order_num)
        if code != '' and num != 0:
            QMessageBox.about(self, "주문", "주문이 요청되었습니다.\n실시간 체결 현황을 확인해주세요")

    def check_balance(self):
        self.kiwoom.reset_opw00018_output()
        account_number = self.comboBox.currentText()

        self.kiwoom.set_input_value("계좌번호", account_number)
        self.kiwoom.comm_rq_data("opw00018_req", "opw00018", 0, "2000")

        while self.kiwoom.remained_data:
            time.sleep(0.2)
            self.kiwoom.set_input_value("계좌번호", account_number)
            self.kiwoom.comm_rq_data("opw00018_req", "opw00018", 2, "2000")

        self.kiwoom.set_input_value("계좌번호", account_number)
        self.kiwoom.comm_rq_data("opw00001_req", "opw00001", 0, "2000")

        item = QTableWidgetItem(self.kiwoom.d2_deposit)
        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.tableWidget.setItem(0, 0, item)

        for i in range(1, 6):
            item = QTableWidgetItem(self.kiwoom.opw00018_output['single'][i-1])
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.tableWidget.setItem(0, i, item)

        self.tableWidget.resizeRowsToContents()

        item_count = len(self.kiwoom.opw00018_output['multi'])
        self.tableWidget_2.setRowCount(item_count)

        for j in range(item_count):
            row = self.kiwoom.opw00018_output['multi'][j]
            for i in range(len(row)):
                item = QTableWidgetItem(row[i])
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.tableWidget_2.setItem(j, i, item)

        self.tableWidget_2.resizeRowsToContents()

    def stacked_0_timeout(self):
        if self.checkBox.isChecked():
            self.check_balance()

            if len(self.kiwoom.chejan_lists) != 0:
                item_count = len(self.kiwoom.chejan_lists)
                self.tableWidget_3.setRowCount(item_count)

                print(self.kiwoom.chejan_lists)

                for i in range(item_count):
                    row = self.kiwoom.chejan_lists[i]
                    for j in range(len(row)):
                        item = QTableWidgetItem(row[j])
                        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                        self.tableWidget_3.setItem(i, j, item)
                self.tableWidget_3.resizeRowsToContents()
                self.tableWidget_3.resizeColumnToContents(0)
                self.tableWidget_3.resizeColumnToContents(1)
                self.tableWidget_3.resizeColumnToContents(2)
                self.tableWidget_3.resizeColumnToContents(4)

    def stacked_1_timeout(self):
        if self.checkBox_2.isChecked():
            self.lineEdit_6.setText(self.kiwoom.real_data[0])
            self.label_41.setText(self.kiwoom.real_data[0])
            self.label_42.setText(self.kiwoom.real_data[1])
            self.label_43.setText(self.kiwoom.real_data[2])
            self.label_44.setText(self.kiwoom.real_data[5])
            self.label_45.setText(self.kiwoom.real_data[6])
            self.label_51.setText(self.kiwoom.real_data[7])
            self.label_52.setText(self.kiwoom.real_data[8])
            self.label_53.setText(self.kiwoom.real_data[9])
            self.label_54.setText(self.kiwoom.real_data[3])
            self.label_55.setText(self.kiwoom.real_data[4])



    # def chejan_data(self):
    #     self.order_num = self.kiwoom.get_chejan_data(9203)
    #     self.item_code = self.kiwoom.get_chejan_data(9001)
    #     self.state = self.kiwoom.get_chejan_data(913)
    #     self.name = self.kiwoom.get_chejan_data(302)
    #     self.order_quantity = self.kiwoom.get_chejan_data(900)
    #     self.order_price = self.kiwoom.get_chejan_data(901)
    #     self.miss_quantity = self.kiwoom.get_chejan_data(903)
    #     self.sell_buy_gubun = self.kiwoom.get_chejan_data(907)
    #
    # def trade_log(self):
    #     # state = self.kiwoom.get_chejan_data(913)
    #     # name = self.kiwoom.get_chejan_data(302)
    #     # sell_buy_gubun = self.kiwoom.get_chejan_data(907)
    #     state = self.kiwoom.state
    #     name = self.kiwoom.name
    #     sell_buy_gubun = self.kiwoom.sell_buy_gubun
    #
    #     list = [state, name, sell_buy_gubun]
    #
    #     for i in range(3):
    #         item = QTableWidgetItem(list[i])
    #         item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
    #         self.tableWidget_3.setItem(0, i, item)
    #
    #     self.tableWidget_3.resizeRowsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    manual_trading = Trading(0)
    manual_trading.show()
    app.exec_()
    app = None
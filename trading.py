"""
화면 번호
1000 - 상한가 / 하한가
2000 - 거래량
4000 - 관심 종목
6000 - 실시간 데이터 처리
"""
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
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
            self.checkBox_2.setEnabled(True)

            self.interest_stock_list = []

            """
            시장 구분 (000:전체, 001:코스피, 101:코스닥)
            정렬 구분 (1:상승률, 2:상승폭, 3:하락률, 4:하락폭)
            정렬 구분 (1:급증량, 2:급증률)
            거래량 구분 (5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상)
            시간 구분 (1:분, 2:전일)
            """
            self.market_gubun = "000"
            self.up_down_gubun = "1"
            self.array_gubun = "2"
            self.volume_gubun = "5"
            self.time_gubun = "2"

            account_num = int(self.kiwoom.get_login_info("ACCOUNT_CNT"))
            accounts = self.kiwoom.get_login_info("ACCNO")
            accounts_list = accounts.split(';')[0:account_num]
            self.comboBox.addItems(accounts_list)

            self.lineEdit.textChanged.connect(self.code_changed)
            self.lineEdit_4.textChanged.connect(self.code_changed_hoga)
            self.lineEdit_7.textChanged.connect(self.code_changed_interest)
            self.lineEdit_7.returnPressed.connect(self.add_interest_stock)

            self.pushButton.clicked.connect(self.send_order)
            self.pushButton_2.clicked.connect(self.check_balance)
            self.pushButton_3.clicked.connect(lambda:self.set_stacked_widget(num=0))
            self.pushButton_4.clicked.connect(lambda:self.set_stacked_widget(num=1))
            self.pushButton_5.clicked.connect(lambda:self.set_stacked_widget(num=2))
            self.pushButton_6.clicked.connect(lambda:self.set_stacked_widget(num=3))
            self.pushButton_7.clicked.connect(lambda:self.set_stacked_widget(num=4))
            self.pushButton_8.clicked.connect(lambda:self.set_stacked_widget(num=5))
            self.pushButton_9.clicked.connect(self.hoga)
            self.pushButton_10.clicked.connect(lambda:self.hoga_clicked(num=10))
            self.pushButton_11.clicked.connect(lambda:self.hoga_clicked(num=11))
            self.pushButton_12.clicked.connect(lambda:self.hoga_clicked(num=12))
            self.pushButton_13.clicked.connect(lambda:self.hoga_clicked(num=13))
            self.pushButton_14.clicked.connect(lambda:self.hoga_clicked(num=14))
            self.pushButton_15.clicked.connect(lambda:self.hoga_clicked(num=15))
            self.pushButton_16.clicked.connect(lambda:self.hoga_clicked(num=16))
            self.pushButton_17.clicked.connect(lambda:self.hoga_clicked(num=17))
            self.pushButton_18.clicked.connect(lambda:self.hoga_clicked(num=18))
            self.pushButton_19.clicked.connect(lambda:self.hoga_clicked(num=19))
            self.pushButton_20.clicked.connect(lambda:self.hoga_clicked(num=20))
            self.pushButton_21.clicked.connect(lambda:self.hoga_clicked(num=21))
            self.pushButton_22.clicked.connect(lambda:self.hoga_clicked(num=22))
            self.pushButton_23.clicked.connect(lambda:self.hoga_clicked(num=23))
            self.pushButton_24.clicked.connect(lambda:self.hoga_clicked(num=24))
            self.pushButton_25.clicked.connect(lambda:self.hoga_clicked(num=25))
            self.pushButton_26.clicked.connect(lambda:self.hoga_clicked(num=26))
            self.pushButton_27.clicked.connect(lambda:self.hoga_clicked(num=27))
            self.pushButton_28.clicked.connect(lambda:self.hoga_clicked(num=28))
            self.pushButton_29.clicked.connect(lambda:self.hoga_clicked(num=29))
            self.pushButton_30.clicked.connect(self.add_interest_stock)
            self.pushButton_31.clicked.connect(self.del_interest_stock)
            self.pushButton_32.clicked.connect(self.remove_real_data)
            self.pushButton_33.clicked.connect(self.surge_volume)
            self.pushButton_34.clicked.connect(self.today_volume_top)
            self.pushButton_35.clicked.connect(self.yesterday_volume_top)
            self.pushButton_36.clicked.connect(self.volume_all_search)

            self.radioButton.clicked.connect(lambda: self.market_change(num=0))
            self.radioButton_2.clicked.connect(lambda: self.market_change(num=1))
            self.radioButton_3.clicked.connect(lambda: self.market_change(num=2))
            self.radioButton_4.clicked.connect(lambda: self.up_down_change(num=0))
            self.radioButton_5.clicked.connect(lambda: self.up_down_change(num=1))
            self.radioButton_6.clicked.connect(lambda: self.market_change(num=0))
            self.radioButton_7.clicked.connect(lambda: self.market_change(num=1))
            self.radioButton_8.clicked.connect(lambda: self.market_change(num=2))
            self.radioButton_9.clicked.connect(lambda: self.array_change(num=0))
            self.radioButton_10.clicked.connect(lambda: self.array_change(num=1))
            # self.tableWidget_4.cellChanged.connect(self.info_interest_stock)

            self.comboBox_3.activated.connect(self.type_changed)
            self.comboBox_2.activated.connect(self.type_order)
            self.comboBox_4.activated.connect(self.volume)
            self.comboBox_5.activated.connect(self.time)

            self.timer_0 = QTimer(self)
            self.timer_0.start(1000*10)
            self.timer_0.timeout.connect(self.stacked_0_timeout)

            self.timer_1 = QTimer(self)
            self.timer_1.start(1000*1)
            self.timer_1.timeout.connect(self.stacked_1_timeout)

            self.timer_2 = QTimer(self)
            self.timer_2.start(1000*1)
            self.timer_2.timeout.connect(self.stacked_2_timeout)
            # 상한가 / 하한가 실시간
            self.timer_3 = QTimer(self)
            self.timer_3.start(1000*4)  ## 1시간 TR 조회 제한까지 커버 가능
            self.timer_3.timeout.connect(self.stacked_3_timeout)
            # 거래량 실시간
            self.timer_4 = QTimer(self)
            self.timer_4.start(1000*4)
            self.timer_4.timeout.connect(self.stacked_4_timeout)
        else:
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.checkBox.setEnabled(False)

    def hoga_clicked(self, num):
        # for i in range(10, 30):
        #     if i == num:
        #         pass
        self.comboBox_3.setCurrentIndex(0)
        if num == 10:
            price = self.pushButton_10.text()
        elif num == 11:
            price = self.pushButton_11.text()
        elif num == 12:
            price = self.pushButton_12.text()
        elif num == 13:
            price = self.pushButton_13.text()
        elif num == 14:
            price = self.pushButton_14.text()
        elif num == 15:
            price = self.pushButton_15.text()
        elif num == 16:
            price = self.pushButton_16.text()
        elif num == 17:
            price = self.pushButton_17.text()
        elif num == 18:
            price = self.pushButton_18.text()
        elif num == 19:
            price = self.pushButton_19.text()
        elif num == 20:
            price = self.pushButton_20.text()
        elif num == 21:
            price = self.pushButton_21.text()
        elif num == 22:
            price = self.pushButton_22.text()
        elif num == 23:
            price = self.pushButton_23.text()
        elif num == 24:
            price = self.pushButton_24.text()
        elif num == 25:
            price = self.pushButton_25.text()
        elif num == 26:
            price = self.pushButton_26.text()
        elif num == 27:
            price = self.pushButton_27.text()
        elif num == 28:
            price = self.pushButton_28.text()
        elif num == 29:
            price = self.pushButton_29.text()
        value = int(price)
        self.spinBox_2.setValue(value)

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
        self.code = code
        # fid_list = "41;51;42;52;27;28;10;11;12;15;13;14;16;17;18"
        che_fid = "10;11;12;27;28;13;14;16;17;18"
        ho_fid = "41;61;51;71;42;62;52;72;43;63;53;73;44;64;54;74;45;65;55;75;46;66;56;76;47;67;57;77;48;68;58;78;49;69;59;79;50;70;60;80;121;125;23;24"
        fid_list = che_fid + ";" + ho_fid
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

        self.checkBox_2.setChecked(True)
        self.pushButton_32.setEnabled(True)
        # self.lineEdit_6.setText(self.kiwoom.real_data[0])
        # self.label_41.setText(self.kiwoom.real_data[0])
        # self.label_42.setText(self.kiwoom.real_data[1])
        # self.label_43.setText(self.kiwoom.real_data[2])
        # self.label_44.setText(self.kiwoom.real_data[5])
        # self.label_45.setText(self.kiwoom.real_data[6])
        # self.label_51.setText(self.kiwoom.real_data[7])
        # self.label_52.setText(self.kiwoom.real_data[8])
        # self.label_53.setText(self.kiwoom.real_data[9])
        # self.label_54.setText(self.kiwoom.real_data[3])
        # self.label_55.setText(self.kiwoom.real_data[4])
        # self.label_22.setText(self.kiwoom.real_data[10])

        ###

    def remove_real_data(self):
        print("remove_real_data")
        code = self.code
        self.kiwoom.set_real_remove(screen_no= 6000, code= code)
        print(code)

    def set_stacked_widget(self, num):
        self.checkBox.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)
        self.radioButton.setChecked(True)
        self.radioButton_4.setChecked(True)
        self.radioButton_6.setChecked(True)
        self.radioButton_9.setChecked(True)

        self.market_change(num=0)
        self.up_down_change(num=0)
        self.array_change(num=0)

        self.kiwoom.set_real_remove("ALL", "ALL")

        if num == 0:
            self.stackedWidget.setCurrentIndex(0)
        elif num == 1:
            self.stackedWidget.setCurrentIndex(1)
        elif num == 2:
            self.stackedWidget.setCurrentIndex(2)
        elif num == 3:
            self.stackedWidget.setCurrentIndex(3)
            self.up_down()
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

    def time(self, index):
        if index == 0:
            time = 1
        elif index == 1:
            time = 2

        self.time_gubun = time
        print(self.time_gubun)

    def volume(self, index):
        if index == 0:
            volume_gubun = "5"
        elif index == 1:
            volume_gubun = "10"
        elif index == 2:
            volume_gubun = "50"
        elif index == 3:
            volume_gubun = "100"
        elif index == 4:
            volume_gubun = "200"
        elif index == 5:
            volume_gubun = "300"
        elif index == 6:
            volume_gubun = "500"
        elif index == 7:
            volume_gubun = "1000"

        self.volume_gubun = volume_gubun
        print(volume_gubun)

    def code_changed(self):
        code = self.lineEdit.text()
        name = self.kiwoom.get_master_code_name(code)
        self.lineEdit_2.setText(name)

    def code_changed_hoga(self):
        code = self.lineEdit_4.text()
        name = self.kiwoom.get_master_code_name(code=code)
        self.lineEdit_5.setText(name)
        self.lineEdit.setText(code)

    def code_changed_interest(self):
        code = self.lineEdit_7.text()
        name = self.kiwoom.get_master_code_name(code=code)
        self.lineEdit_8.setText(name)

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

        if code != '' and num != 0:
             self.kiwoom.send_order("send_order_req", "0101", account, order_type_lookup[order_type], code, num, price,
                                    hoga_lookup[hoga], order_num)
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
            color, data = self.color_2(self.kiwoom.opw00018_output['single'][i-1])
            item = QTableWidgetItem(data)

            if color == "red":
                item.setForeground(QtGui.QBrush(Qt.red))
            elif color == "blue":
                item.setForeground(QtGui.QBrush(Qt.blue))
            else:
                item.setForeground(QtGui.QBrush(Qt.black))
            self.tableWidget.setItem(0, i, item)

        self.tableWidget.resizeRowsToContents()

        # for i in range(1, 6):
        #     item = QTableWidgetItem(self.kiwoom.opw00018_output['single'][i-1])
        #     item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        #     self.tableWidget.setItem(0, i, item)
        #
        # self.tableWidget.resizeRowsToContents()

        item_count = len(self.kiwoom.opw00018_output['multi'])
        self.tableWidget_2.setRowCount(item_count)

        for i in range(item_count):
            for count, stock in enumerate(self.kiwoom.opw00018_output['multi'][i]):
                color, data = self.color_2(stock)
                item = QTableWidgetItem(data)

                if count >= 4:
                    if color == "red":
                        item.setForeground(QtGui.QBrush(Qt.red))
                    elif color == "blue":
                        item.setForeground(QtGui.QBrush(Qt.blue))
                    else:
                        item.setForeground(QtGui.QBrush(Qt.red))
                elif count < 4:
                    item.setForeground(QtGui.QBrush(Qt.black))

                self.tableWidget_2.setItem(i, count, item)

        self.tableWidget_2.resizeRowsToContents()
        self.tableWidget_2.resizeRowsToContents()

        # for j in range(item_count):
        #     row = self.kiwoom.opw00018_output['multi'][j]
        #     for i in range(len(row)):
        #         item = QTableWidgetItem(row[i])
        #         item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        #         self.tableWidget_2.setItem(j, i, item)
        #
        # self.tableWidget_2.resizeRowsToContents()


    def add_interest_stock(self):
        if self.lineEdit_8.text() != "":
            stock_list = []
            if len(self.interest_stock_list) == 0:
                code = self.lineEdit_7.text()
                name = self.lineEdit_8.text()

                stock_list.append(code)
                stock_list.append(name)
                self.interest_stock_list.append(stock_list)

                list_count = len(self.interest_stock_list)
                self.tableWidget_4.setRowCount(list_count)

                for i in range(list_count):
                    for count, item in enumerate(self.interest_stock_list[i]):
                        item = QTableWidgetItem(item)
                        self.tableWidget_4.setItem(i, count, item)
                        print(i,count)

                # self.tableWidget_4.setItem(0, 0, code)
                # self.tableWidget_4.setItem(0, 1, name)

                # self.tableWidget_4.cellChanged.connect(self.info_interest_stock)

                self.tableWidget_4.resizeRowsToContents()
                self.tableWidget_4.resizeColumnsToContents()

                self.info_interest_stock()
            else:
                code = self.lineEdit_7.text()
                name = ""

                for i, stock in enumerate(self.interest_stock_list):
                    if stock[0] == code:
                        name = ""
                        QMessageBox.about(self, "오류", "이미 추가된 종목입니다.")
                        break
                    else:
                        name = self.lineEdit_8.text()

                if name == "":
                    pass
                else:
                    stock_list.append(code)
                    stock_list.append(name)
                    self.interest_stock_list.append(stock_list)

                    list_count = len(self.interest_stock_list)
                    self.tableWidget_4.setRowCount(list_count)

                    for i in range(list_count):
                        for count, item in enumerate(self.interest_stock_list[i]):
                            item = QTableWidgetItem(item)
                            self.tableWidget_4.setItem(i, count, item)

                    # self.tableWidget_4.setItem(0, 0, code)
                    # self.tableWidget_4.setItem(0, 1, name)

                    self.tableWidget_4.resizeRowsToContents()
                    self.tableWidget_4.resizeColumnsToContents()

                    self.info_interest_stock()
        else:
            QMessageBox.about(self, "오류", "정상적인 종목코드를 입력하세요")

    def del_interest_stock(self):
        if self.lineEdit_8.text() != "":
            stock_list = []
            if len(self.interest_stock_list) == 0:
                QMessageBox.about(self, "오류", "등록된 관심종목이 없습니다.")
            else:
                code = self.lineEdit_7.text()
                name = self.lineEdit_8.text()
                stock_list.append(code)
                stock_list.append(name)

                for stock in self.interest_stock_list:
                    if stock[0] == code:
                        self.interest_stock_list.remove(stock_list)
                    else:
                        pass

                line_count = len(self.interest_stock_list)
                self.tableWidget_4.setRowCount(line_count)

                for i in range(line_count):
                    for count, item in enumerate(self.interest_stock_list[i]):
                        item = QTableWidgetItem(item)
                        self.tableWidget_4.setItem(i, count, item)

                self.tableWidget_4.resizeRowsToContents()
                self.tableWidget_4.resizeColumnsToContents()

                self.info_interest_stock()
        else:
            QMessageBox.about(self, "오류", "정상적인 종목코드를 입력하세요")

    def info_interest_stock(self):
        cnt = len(self.interest_stock_list)

        if self.interest_stock_list[0][0] == "":
            pass
        else:
            code = self.interest_stock_list[0][0]
            print("cnt = " + str(cnt))
            for i in range(1, cnt):
                code = code + ';' + self.interest_stock_list[i][0]

            self.kiwoom.comm_kw_rq_data(code, cnt, 4000)

            # self.kiwoom.info_list
            print(self.kiwoom.info_list)
            self.tableWidget_5.setRowCount(cnt)

            for i in range(cnt):
                for count, info in enumerate(self.kiwoom.info_list[i]):
                    color, data = self.color_2(info)
                    item = QTableWidgetItem(data)
                    if color == "red":
                        item.setForeground(QtGui.QBrush(Qt.red))
                    elif color == "blue":
                        item.setForeground(QtGui.QBrush(Qt.blue))
                    else:
                        item.setForeground(QtGui.QBrush(Qt.black))
                    # item.setBackground(QtGui.QColor(255, 0, 0))
                    # item.setForeground(QtGui.QBrush(Qt.blue))
                    print("Trading info", info)
                    self.tableWidget_5.setItem(i, count, item)

            # self.tableWidget_4.setItem(0, 0, code)
            # self.tableWidget_4.setItem(0, 1, name)

            self.tableWidget_5.resizeRowsToContents()
            self.tableWidget_5.resizeColumnsToContents()

    def up_down(self):
        """
        시장구분 = 000:전체, 001:코스피, 101:코스닥
        정렬구분 = 1:상승률, 2:상승폭, 3:하락률, 4:하락폭
        거래량조건 = 0000:전체조회, 0010:만주이상, 0050:5만주이상, 0100:10만주이상, 0150:15만주이상, 0200:20만주이상, 0300:30만주이상, 0500:50만주이상, 1000:백만주이상
        종목조건 = 0:전체조회, 1:관리종목제외, 4:우선주+관리주제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 11:정리매매종목제외
        신용조건 = 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 9:신용융자전체
        상하한포함 = 0:불 포함, 1:포함
        가격조건 = 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~5천원, 4:5천원~1만원, 5:1만원이상, 8:1천원이상
        거래대금조건 = 0:전체조회, 3:3천만원이상, 5:5천만원이상, 10:1억원이상, 30:3억원이상, 50:5억원이상, 100:10억원이상, 300:30억원이상, 500:50억원이상, 1000:100억원이상, 3000:300억원이상, 5000:500억원이상
        """

        market_gubun = self.market_gubun
        up_down_gubun = self.up_down_gubun

        volume_condition = "0000"
        stock_condition = "0"
        credit_condition = "0"
        in_up_down = "1"
        price_condition = "0"
        trading_price_condition = "0"

        self.kiwoom.set_input_value("시장구분", market_gubun)
        self.kiwoom.set_input_value("정렬구분", up_down_gubun)
        self.kiwoom.set_input_value("거래량조건", volume_condition)
        self.kiwoom.set_input_value("종목조건", stock_condition)
        self.kiwoom.set_input_value("신용조건", credit_condition)
        self.kiwoom.set_input_value("상한가포함", in_up_down)
        self.kiwoom.set_input_value("가격조건", price_condition)
        self.kiwoom.set_input_value("거래대금조건", trading_price_condition)

        self.kiwoom.comm_rq_data(rqname="opt10027_req", trcode="opt10027", next="0", screen_no="1000")

        ## 데이터 받고 가공 시작

        # self.kiwoom.up_stock_list

        cnt = len(self.kiwoom.up_stock_list)

        self.tableWidget_6.setRowCount(cnt)

        for i in range(cnt):
            for count, stock in enumerate(self.kiwoom.up_stock_list[i]):
                color, data = self.color_2(stock)
                item = QTableWidgetItem(data)

                if color == "red":
                    item.setForeground(QtGui.QBrush(Qt.red))
                elif color == "blue":
                    item.setForeground(QtGui.QBrush(Qt.blue))
                else:
                    item.setForeground(QtGui.QBrush(Qt.black))
                self.tableWidget_6.setItem(i, count, item)

        self.tableWidget_6.resizeRowsToContents()
        self.tableWidget_6.resizeColumnsToContents()

        cnt = len(self.kiwoom.up_near_stock_list)

        self.tableWidget_7.setRowCount(cnt)

        for i in range(cnt):
            for count, stock in enumerate(self.kiwoom.up_near_stock_list[i]):
                color, data = self.color_2(stock)
                item = QTableWidgetItem(data)

                if color == "red":
                    item.setForeground(QtGui.QBrush(Qt.red))
                elif color == "blue":
                    item.setForeground(QtGui.QBrush(Qt.blue))
                else:
                    item.setForeground(QtGui.QBrush(Qt.black))
                self.tableWidget_7.setItem(i, count, item)

        self.tableWidget_7.resizeRowsToContents()
        self.tableWidget_7.resizeColumnsToContents()

    def surge_volume(self):
        """
        시장구분 = 000:전체, 001:코스피, 101:코스닥
        정렬구분 = 1:급증량, 2:급증률
        시간구분 = 1:분, 2:전일
        거래량구분 = 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상
        시간 = 분 입력
        종목조건 = 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기
        가격구분 = 0:전체조회, 2:5만원이상, 5:1만원이상, 6:5천원이상, 8:1천원이상, 9:10만원이상
        """
        market_gubun = self.market_gubun
        array_gubun = self.array_gubun
        time_gubun = self.time_gubun
        volume_gubun = self.volume_gubun

        time = "0"
        stock_condition = "0"
        price_gubun = "0"

        self.kiwoom.set_input_value(id="시장구분", value=market_gubun)
        self.kiwoom.set_input_value(id="정렬구분", value=array_gubun)
        self.kiwoom.set_input_value(id="시간구분", value=time_gubun)
        self.kiwoom.set_input_value(id="거래량구분", value=volume_gubun)
        self.kiwoom.set_input_value(id="시간", value=time)
        self.kiwoom.set_input_value(id="종목조건", value=stock_condition)
        self.kiwoom.set_input_value(id="가격구분", value=price_gubun)

        self.kiwoom.comm_rq_data(rqname="OPT10023_req", trcode="OPT10023", next="0", screen_no="2000")

        # 데이터 받기 전
        ##############
        # 데이터 받은 후

        cnt = len(self.kiwoom.surge_volume_list)
        self.tableWidget_9.setRowCount(cnt)

        for i in range(cnt):
            for count, stock in enumerate(self.kiwoom.surge_volume_list[i]):
                color, data = self.color_2(stock)
                item = QTableWidgetItem(data)

                if color == "red":
                    item.setForeground(QtGui.QBrush(Qt.red))
                elif color == "blue":
                    item.setForeground(QtGui.QBrush(Qt.blue))
                else:
                    item.setForeground(QtGui.QBrush(Qt.black))
                self.tableWidget_9.setItem(i, count, item)
        self.tableWidget_9.resizeRowsToContents()
        self.tableWidget_9.resizeColumnsToContents()

    def today_volume_top(self):
        """
        시장구분 = 000:전체, 001:코스피, 101:코스닥
        정렬구분 = 1:거래량, 2:거래회전율, 3:거래대금
        관리종목포함 = 0:관리종목 포함, 1:관리종목 미포함, 3:우선주제외, 11:정리매매종목제외, 4:관리종목, 우선주제외, 5:증100제외, 6:증100마나보기, 13:증60만보기, 12:증50만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 14:ETF제외, 15:스팩제외, 16:ETF+ETN제외
        신용구분 = 0:전체조회, 9:신용융자전체, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 8:신용대주
        거래량구분 = 0:전체조회, 5:5천주이상, 10:1만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:500만주이상, 1000:백만주이상
        가격구분 = 0:전체조회, 1:1천원미만, 2:1천원이상, 3:1천원~2천원, 4:2천원~5천원, 5:5천원이상, 6:5천원~1만원, 10:1만원미만, 7:1만원이상, 8:5만원이상, 9:10만원이상
        거래대금구분 = 0:전체조회, 1:1천만원이상, 3:3천만원이상, 4:5천만원이상, 10:1억원이상, 30:3억원이상, 50:5억원이상, 100:10억원이상, 300:30억원이상, 500:50억원이상, 1000:100억원이상, 3000:300억원이상, 5000:500억원이상
        장운영구분 = 0:전체조회, 1:장중, 999:시간외전체, 2:장전시간외, 3:장후시간외
        """
        market_gubun = self.market_gubun
        array_gubun = "1"
        volume_gubun = self.volume_gubun

        management_item = "0"
        credit_gubun = "0"
        price_gubun = "0"
        trade_payment = "0"
        market_manage_gubun = "0"

        self.kiwoom.set_input_value(id="시장구분", value=market_gubun)
        self.kiwoom.set_input_value(id="정렬구분", value=array_gubun)
        self.kiwoom.set_input_value(id="관리종목포함", value=management_item)
        self.kiwoom.set_input_value(id="신용구분", value=credit_gubun)
        self.kiwoom.set_input_value(id="거래량구분", value=volume_gubun)
        self.kiwoom.set_input_value(id="가격구분", value=price_gubun)
        self.kiwoom.set_input_value(id="거래대금구분", value=trade_payment)
        self.kiwoom.set_input_value(id="장운영구분", value=market_manage_gubun)

        self.kiwoom.comm_rq_data(rqname="opt10030_req", trcode="opt10030", next="0", screen_no="2100")

        # 데이터 받기 전
        ##############
        # 데이터 받은 후

        cnt = len(self.kiwoom.today_volume_top)
        self.tableWidget_10.setRowCount(cnt)

        for i in range(cnt):
            for count, stock in enumerate(self.kiwoom.today_volume_top[i]):
                color, data = self.color_2(stock)
                item = QTableWidgetItem(data)

                if color == "red":
                    item.setForeground(QtGui.QBrush(Qt.red))
                elif color == "blue":
                    item.setForeground(QtGui.QBrush(Qt.blue))
                else:
                    item.setForeground(QtGui.QBrush(Qt.black))
                self.tableWidget_10.setItem(i, count, item)
        self.tableWidget_10.resizeRowsToContents()
        self.tableWidget_10.resizeColumnsToContents()

    def yesterday_volume_top(self):
        """
        시장구분 = 000:전체, 001:코스피, 101:코스닥
        조회구분 = 1:전일거래량 상위100종목, 2:전일거래대금 상위100종목
        순위시작 = 0 ~ 100 값 중에  조회를 원하는 순위 시작값
        순위끝 = 0 ~ 100 값 중에  조회를 원하는 순위 끝값
        """
        market_gubun = self.market_gubun

        search_gubun = "1"
        rank_start = "0"
        rank_end = "100"

        self.kiwoom.set_input_value(id="시장구분", value=market_gubun)
        self.kiwoom.set_input_value(id="조회구분", value=search_gubun)
        self.kiwoom.set_input_value(id="순위시작", value=rank_start)
        self.kiwoom.set_input_value(id="순위끝", value=rank_end)

        self.kiwoom.comm_rq_data(rqname="OPT10031_req", trcode="OPT10031", next="0", screen_no="2200")

        # 데이터 받기 전
        ##############
        # 데이터 받은 후

        cnt = len(self.kiwoom.yesterday_volume_top)
        self.tableWidget_11.setRowCount(cnt)

        for i in range(cnt):
            for count, stock in enumerate(self.kiwoom.yesterday_volume_top[i]):
                color, data = self.color_2(stock)
                item = QTableWidgetItem(data)

                if color == "red":
                    item.setForeground(QtGui.QBrush(Qt.red))
                elif color == "blue":
                    item.setForeground(QtGui.QBrush(Qt.blue))
                else:
                    item.setForeground(QtGui.QBrush(Qt.black))
                self.tableWidget_11.setItem(i, count, item)
        self.tableWidget_11.resizeRowsToContents()
        self.tableWidget_11.resizeColumnsToContents()

    def volume_all_search(self):
        self.surge_volume()
        self.today_volume_top()
        self.yesterday_volume_top()

    def market_change(self, num):
        if num == 0:
            market_gubun = "000"
        elif num == 1:
            market_gubun = "001"
        elif num == 2:
            market_gubun = "101"
        self.market_gubun = market_gubun

        # self.up_down()

    def up_down_change(self, num):
        if num == 0:
            up_down_gubun = "1"
        elif num == 1:
            up_down_gubun = "3"
        self.up_down_gubun = up_down_gubun

        self.up_down()

    def array_change(self, num):
        if num == 0:
            array_gubun = "2"
        elif num == 1:
            array_gubun = "1"
        self.array_gubun = array_gubun


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
            if self.lineEdit_5.text() != "":
                color, str = self.color(self.kiwoom.real_data[0])
                self.lineEdit_6.setStyleSheet(color)
                self.lineEdit_6.setText(str)
                self.label_41.setStyleSheet(color)
                self.label_41.setText(str)
                color, str = self.color(self.kiwoom.real_data[1])
                self.label_42.setStyleSheet(color)
                self.label_42.setText(str)
                color, str = self.color(self.kiwoom.real_data[2])
                self.label_43.setStyleSheet(color)
                self.label_43.setText(str)
                color, str = self.color(self.kiwoom.real_data[5])
                self.label_44.setStyleSheet(color)
                self.label_44.setText(self.kiwoom.real_data[5])
                color, str = self.color(self.kiwoom.real_data[6])
                self.label_45.setStyleSheet(color)
                self.label_45.setText(str)
                color, str = self.color(self.kiwoom.real_data[7])
                self.label_51.setStyleSheet(color)
                self.label_51.setText(str)
                color, str = self.color(self.kiwoom.real_data[8])
                self.label_52.setStyleSheet(color)
                self.label_52.setText(str)
                color, str = self.color(self.kiwoom.real_data[9])
                self.label_53.setStyleSheet(color)
                self.label_53.setText(str)
                color, str = self.color(self.kiwoom.real_data[3])
                self.label_54.setStyleSheet(color)
                self.label_54.setText(str)
                color, str = self.color(self.kiwoom.real_data[4])
                self.label_55.setStyleSheet(color)
                self.label_55.setText(str)
                color, str = self.color(self.kiwoom.real_data[10])
                self.label_23.setStyleSheet(color)
                self.label_23.setText(self.kiwoom.real_data[10])

                color, str = self.color(self.kiwoom.real_hoga[1][9])
                self.pushButton_10.setStyleSheet(color)
                self.pushButton_10.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[1][8])
                self.pushButton_11.setStyleSheet(color)
                self.pushButton_11.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[1][7])
                self.pushButton_12.setStyleSheet(color)
                self.pushButton_12.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[1][6])
                self.pushButton_13.setStyleSheet(color)
                self.pushButton_13.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[1][5])
                self.pushButton_14.setStyleSheet(color)
                self.pushButton_14.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[1][4])
                self.pushButton_15.setStyleSheet(color)
                self.pushButton_15.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[1][3])
                self.pushButton_16.setStyleSheet(color)
                self.pushButton_16.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[1][2])
                self.pushButton_17.setStyleSheet(color)
                self.pushButton_17.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[1][1])
                self.pushButton_18.setStyleSheet(color)
                self.pushButton_18.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[1][0])
                self.pushButton_19.setStyleSheet(color)
                self.pushButton_19.setText(str)

                color, str = self.color(self.kiwoom.real_hoga[3][0])
                self.pushButton_20.setStyleSheet(color)
                self.pushButton_20.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[3][1])
                self.pushButton_21.setStyleSheet(color)
                self.pushButton_21.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[3][2])
                self.pushButton_22.setStyleSheet(color)
                self.pushButton_22.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[3][3])
                self.pushButton_23.setStyleSheet(color)
                self.pushButton_23.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[3][4])
                self.pushButton_24.setStyleSheet(color)
                self.pushButton_24.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[3][5])
                self.pushButton_25.setStyleSheet(color)
                self.pushButton_25.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[3][6])
                self.pushButton_26.setStyleSheet(color)
                self.pushButton_26.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[3][7])
                self.pushButton_27.setStyleSheet(color)
                self.pushButton_27.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[3][8])
                self.pushButton_28.setStyleSheet(color)
                self.pushButton_28.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[3][9])
                self.pushButton_29.setStyleSheet(color)
                self.pushButton_29.setText(str)

                color, str = self.color(self.kiwoom.real_hoga[2][9])
                self.label_70.setStyleSheet(color)
                self.label_70.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[2][8])
                self.label_71.setStyleSheet(color)
                self.label_71.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[2][7])
                self.label_72.setStyleSheet(color)
                self.label_72.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[2][6])
                self.label_73.setStyleSheet(color)
                self.label_73.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[2][5])
                self.label_74.setStyleSheet(color)
                self.label_74.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[2][4])
                self.label_75.setStyleSheet(color)
                self.label_75.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[2][3])
                self.label_76.setStyleSheet(color)
                self.label_76.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[2][2])
                self.label_77.setStyleSheet(color)
                self.label_77.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[2][1])
                self.label_78.setStyleSheet(color)
                self.label_78.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[2][0])
                self.label_79.setStyleSheet(color)
                self.label_79.setText(str)

                color, str = self.color(self.kiwoom.real_hoga[4][0])
                self.label_80.setStyleSheet(color)
                self.label_80.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[4][1])
                self.label_81.setStyleSheet(color)
                self.label_81.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[4][2])
                self.label_82.setStyleSheet(color)
                self.label_82.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[4][3])
                self.label_83.setStyleSheet(color)
                self.label_83.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[4][4])
                self.label_84.setStyleSheet(color)
                self.label_84.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[4][5])
                self.label_85.setStyleSheet(color)
                self.label_85.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[4][6])
                self.label_86.setStyleSheet(color)
                self.label_86.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[4][7])
                self.label_87.setStyleSheet(color)
                self.label_87.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[4][8])
                self.label_88.setStyleSheet(color)
                self.label_88.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[4][9])
                self.label_89.setStyleSheet(color)
                self.label_89.setText(str)

                color, str = self.color(self.kiwoom.real_hoga[0][0])
                self.label_62.setStyleSheet(color)
                self.label_62.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[0][1])
                self.label_64.setStyleSheet(color)
                self.label_64.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[0][2])
                self.label_59.setStyleSheet(color)
                self.label_59.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[0][3])
                self.label_61.setStyleSheet(color)
                self.label_61.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[0][4])
                self.label_63.setStyleSheet(color)
                self.label_63.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[0][5])
                self.label_60.setStyleSheet(color)
                self.label_60.setText(self.kiwoom.real_hoga[0][5])
                color, str = self.color(self.kiwoom.real_hoga[0][6])
                self.label_58.setStyleSheet(color)
                self.label_58.setText(self.kiwoom.real_hoga[0][6])
                color, str = self.color(self.kiwoom.real_hoga[0][7])
                self.label_18.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[0][8])
                self.label_19.setText(str)
                color, str = self.color(self.kiwoom.real_hoga[0][9])
                self.label_21.setStyleSheet(color)
                self.label_21.setText(str)

                # self.lineEdit_6.setText(self.kiwoom.real_data[0])
                # # if color == "red":
                # #     self.label_41.setStyleSheet("color: red;")
                # #     self.label_41.setText(self.kiwoom.real_data[0])
                # self.label_41.setStyleSheet("color: " + color + ";")
                # self.label_41.setText(str)
                #
                # self.label_42.setText(self.kiwoom.real_data[1])
                # self.label_43.setText(self.kiwoom.real_data[2])
                # self.label_44.setText(self.kiwoom.real_data[5])
                # self.label_45.setText(self.kiwoom.real_data[6])
                # self.label_51.setText(self.kiwoom.real_data[7])
                # self.label_52.setText(self.kiwoom.real_data[8])
                # self.label_53.setText(self.kiwoom.real_data[9])
                # self.label_54.setText(self.kiwoom.real_data[3])
                # self.label_55.setText(self.kiwoom.real_data[4])
                #
                # self.pushButton_10.setText(self.kiwoom.real_hoga[1][9])
                # self.pushButton_11.setText(self.kiwoom.real_hoga[1][8])
                # self.pushButton_12.setText(self.kiwoom.real_hoga[1][7])
                # self.pushButton_13.setText(self.kiwoom.real_hoga[1][6])
                # self.pushButton_14.setText(self.kiwoom.real_hoga[1][5])
                # self.pushButton_15.setText(self.kiwoom.real_hoga[1][4])
                # self.pushButton_16.setText(self.kiwoom.real_hoga[1][3])
                # self.pushButton_17.setText(self.kiwoom.real_hoga[1][2])
                # self.pushButton_18.setText(self.kiwoom.real_hoga[1][1])
                # self.pushButton_19.setText(self.kiwoom.real_hoga[1][0])
                #
                # self.pushButton_20.setText(self.kiwoom.real_hoga[3][0])
                # self.pushButton_21.setText(self.kiwoom.real_hoga[3][1])
                # self.pushButton_22.setText(self.kiwoom.real_hoga[3][2])
                # self.pushButton_23.setText(self.kiwoom.real_hoga[3][3])
                # self.pushButton_24.setText(self.kiwoom.real_hoga[3][4])
                # self.pushButton_25.setText(self.kiwoom.real_hoga[3][5])
                # self.pushButton_26.setText(self.kiwoom.real_hoga[3][6])
                # self.pushButton_27.setText(self.kiwoom.real_hoga[3][7])
                # self.pushButton_28.setText(self.kiwoom.real_hoga[3][8])
                # self.pushButton_29.setText(self.kiwoom.real_hoga[3][9])
                #
                # self.label_70.setText(self.kiwoom.real_hoga[2][9])
                # self.label_71.setText(self.kiwoom.real_hoga[2][8])
                # self.label_72.setText(self.kiwoom.real_hoga[2][7])
                # self.label_73.setText(self.kiwoom.real_hoga[2][6])
                # self.label_74.setText(self.kiwoom.real_hoga[2][5])
                # self.label_75.setText(self.kiwoom.real_hoga[2][4])
                # self.label_76.setText(self.kiwoom.real_hoga[2][3])
                # self.label_77.setText(self.kiwoom.real_hoga[2][2])
                # self.label_78.setText(self.kiwoom.real_hoga[2][1])
                # self.label_79.setText(self.kiwoom.real_hoga[2][0])
                #
                # self.label_80.setText(self.kiwoom.real_hoga[4][0])
                # self.label_81.setText(self.kiwoom.real_hoga[4][1])
                # self.label_82.setText(self.kiwoom.real_hoga[4][2])
                # self.label_83.setText(self.kiwoom.real_hoga[4][3])
                # self.label_84.setText(self.kiwoom.real_hoga[4][4])
                # self.label_85.setText(self.kiwoom.real_hoga[4][5])
                # self.label_86.setText(self.kiwoom.real_hoga[4][6])
                # self.label_87.setText(self.kiwoom.real_hoga[4][7])
                # self.label_88.setText(self.kiwoom.real_hoga[4][8])
                # self.label_89.setText(self.kiwoom.real_hoga[4][9])
                #
                # self.label_62.setText(self.kiwoom.real_hoga[0][0])
                # self.label_64.setText(self.kiwoom.real_hoga[0][1])
                # self.label_59.setText(self.kiwoom.real_hoga[0][2])
                # self.label_61.setText(self.kiwoom.real_hoga[0][3])
                # self.label_63.setText(self.kiwoom.real_hoga[0][4])
                # self.label_60.setText(self.kiwoom.real_hoga[0][5])
                # self.label_58.setText(self.kiwoom.real_hoga[0][6])
                # self.label_18.setText(self.kiwoom.real_hoga[0][7])
                # self.label_19.setText(self.kiwoom.real_hoga[0][8])
                # self.label_21.setText(self.kiwoom.real_hoga[0][9])

    def stacked_2_timeout(self):
        if self.checkBox_3.isChecked():
            # self.kiwoom.interest_data
            print(self.interest_stock_list)
            cnt = len(self.interest_stock_list)
            print(cnt)
            self.tableWidget_5.setRowCount(cnt)
            try:
                for i in range(cnt):
                    if self.kiwoom.interest_data[0] == self.interest_stock_list[i][0]:
                        for count, info in enumerate(self.kiwoom.interest_data):
                            color, data = self.color_2(info)
                            item = QTableWidgetItem(data)
                            if color == "red":
                                item.setForeground(QtGui.QBrush(Qt.red))
                            elif color == "blue":
                                item.setForeground(QtGui.QBrush(Qt.blue))
                            else:
                                item.setForeground(QtGui.QBrush(Qt.black))
                            self.tableWidget_5.setItem(i, count, item)
            except AttributeError as e:
                print("장마감")
                QMessageBox.about(self, "장 마감", "개장시에만 동작합니다.")
                self.checkBox_3.setChecked(False)


            # self.tableWidget_4.setItem(0, 0, code)
            # self.tableWidget_4.setItem(0, 1, name)

            self.tableWidget_5.resizeRowsToContents()
            self.tableWidget_5.resizeColumnsToContents()

    def stacked_3_timeout(self):
        if self.checkBox_4.isChecked():
            self.up_down()

    def stacked_4_timeout(self):
        if self.checkBox_5.isChecked():
            self.surge_volume()
            self.today_volume_top()
            self.yesterday_volume_top()

    def color(self, str):
        if str.startswith('+'):
            color = "red"
            num = str[1:]
        elif str.startswith('-'):
            color = "blue"
            num = str[1:]
        else:
            color = "black"
            num = str[1:]
        color = "color: " + color + ";"
        return color, num

    def color_2(self, str):
        if str.startswith('+'):
            color = "red"
            data = str[1:]
        elif str.startswith('-'):
            color = "blue"
            data = str[1:]
        else:
            color = "black"
            data = str
        return color, data

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
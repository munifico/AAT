"""
현재 시간을 출력하는 기능은 일정한 단위로 현재 시간을 얻어온 후 이를 StatusBar에 출력.
이를 위해서는 주기적으로 이벤트를 발생시키는 Timer가 필요.
Timer가 1초에 한 번 이벤트(시그널)을 발생시키면 이 이멘트를 처리하는 메서드(슬롯)에서 현재 시간을 얻어온 후 이를 StatusBar에 출력

Qt 의 QTimer 클래스를 사용하면 정해진 시간마다 이벤트를 발생시킬 수 있다.
QTimer 클래스
메서드 start - 이 메서드에 인자로 1000을 지정하면 1초에 한 번씩 주기적으로 timeout 시그널이 발생.

시그널을 처리할 슬롯에서는.
timeout 메서드에서는 현재 시간을 구하고, 시간:분:초 형태의 문자열로 변환.
Kiwoom 클래스의 get_connect_state 메서드를 호출해서 서버 연결 상태를 확인한 후
시간과 상태 출력 메시지를 StatusBar 위젯에 출력.

키움 OpenAPI는 비밀번호를 저장받아서 자동 로그인이 된다.
"""

"""
Qt Designer에서 위젯을 선택한 다음 속성편집기 -> objectName 항복의 이름으로 위젯 컨트롤

self.lineEdit.textChanged.connect(self.code_changed)
시그널 -> 슬롯을 설정했기 때문에 textChanged 이벤트가 발생하면 code_changed 메서드 호출


"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Kiwoom import *

form_class = uic.loadUiType("pytrader.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.trade_stocks_done = False

        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)

        self.lineEdit.textChanged.connect(self.code_changed)

        accounts_num = int(self.kiwoom.get_login_info("ACCOUNT_CNT"))
        accounts = self.kiwoom.get_login_info("ACCNO")
        print(accounts+'\n')
        accounts_list = accounts.split(';')[0:accounts_num]
        self.comboBox.addItems(accounts_list)
        print(accounts_list)
        self.pushButton.clicked.connect(self.send_order)

        self.pushButton_2.clicked.connect(self.check_balance)

        self.timer2 = QTimer(self)
        self.timer2.start(1000*10)
        self.timer2.timeout.connect(self.timeout2)

        self.load_buy_sell_list()


    def trade_stocks(self):
        hoga_lookup = {'지정가': "00", '시장가': "03"}

        f = open("buy_list.txt", 'rt', encoding='UTF8')
        buy_list = f.readlines()
        f.close()

        f = open("sell_list.txt", 'rt', encoding='UTF8')
        sell_list = f.readlines()
        f.close()

        account = self.comboBox.currentText()

        for row_data in buy_list:
            split_row_data = row_data.split(';')
            hoga = split_row_data[2]
            code = split_row_data[1]
            num = split_row_data[3]
            price = split_row_data[4]

            if split_row_data[-1].rstrip() == '매수전':
                self.kiwoom.send_order("send_order_req", "0101", account, 1, code, num, price, hoga_lookup[hoga], "")

        for row_data in sell_list:
            split_row_data = row_data.split(';')
            hoga = split_row_data[2]
            code = split_row_data[1]
            num = split_row_data[3]
            price = split_row_data[4]

            if split_row_data[-1].rstrip() == '매도전':
                self.kiwoom.send_order("send_order_req", "0101", account, 2, code, num, price, hoga_lookup[hoga], "")

        for i,row_data in enumerate(buy_list):
            buy_list[i] = buy_list[i].replace("매수전", "주문완료")

        f = open("buy_list.txt", 'wt', encoding='UTF8')

        for row_data in buy_list:
            f.write(row_data)
        f.close()

        for i, row_data in enumerate(sell_list):
            sell_list[i] = sell_list[i].replace("매도전", "주문완료")

        f = open("sell_list.txt", 'wt', encoding='UTF8')

        for row_data in sell_list:
            f.write(row_data)
        f.close()



    def timeout(self):
        market_start_time = QTime(9, 0, 0)
        current_time = QTime.currentTime()

        if current_time > market_start_time and self.trade_stocks_done is False:
            self.trade_stocks()
            self.trade_stocks_done = True

        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간 : " + text_time

        state = self.kiwoom.get_connect_state()

        if state == 1:
            state_msg = "서버 연결 중"
        else:
            state_msg = "서버 미 연결 중"

        self.statusBar().showMessage(state_msg + " | " + time_msg)


    def load_buy_sell_list(self):
        f = open("buy_list.txt", 'rt', encoding='UTF8')
        buy_list = f.readlines()
        f.close()

        f = open("sell_list.txt", 'rt', encoding='UTF8')
        sell_list = f.readlines()
        f.close()

        row_count = len(buy_list) + len(sell_list)
        self.tableWidget_3.setRowCount(row_count)

        for j in range(len(buy_list)):
            row_data = buy_list[j]
            split_row_data = row_data.split(';')
            split_row_data[1] = self.kiwoom.get_master_code_name(split_row_data[1].rsplit())

            for i in range(len(split_row_data)):
                item = QTableWidgetItem(split_row_data[i].rstrip())
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                self.tableWidget_3.setItem(j, i, item)

        for j in range(len(sell_list)):
            row_data = sell_list[j]
            split_row_data = row_data.split(';')
            split_row_data[1] = self.kiwoom.get_master_code_name(split_row_data[1].rstrip())

            for i in range(len(split_row_data)):
                item = QTableWidgetItem(split_row_data[i].rstrip())
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                self.tableWidget_3.setItem(len(buy_list) + j, i, item)

        self.tableWidget_3.resizeRowsToContents()


    def timeout2(self):
        if self.checkBox.isChecked():
            self.check_balance()

    def check_balance(self):
        self.kiwoom.reset_opw00018_output()
        account_number = self.kiwoom.get_login_info("ACCNO")
        account_number = account_number.split(';')[0]

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


    def code_changed(self):
        code = self.lineEdit.text()
        name = self.kiwoom.get_master_code_name(code)
        self.lineEdit_2.setText(name)

    def send_order(self):
        order_type_lookup = {'신규매수': 1, '신규매도': 2, '매수취소': 3,'매도취소': 4}
        hoga_lookup = {'지정가': '00', '시장가': '03'}

        account = self.comboBox.currentText()
        order_type = self.comboBox_2.currentText()
        code = self.lineEdit.text()
        hoga = self.comboBox_3.currentText()
        num = self.spinBox.value()
        price = self.spinBox_2.value()

        self.kiwoom.send_order("send_order_req", "0101", account, order_type_lookup[order_type], code, num, price, hoga_lookup[hoga], "")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
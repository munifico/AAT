from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from kiwoom import *
import time

form_class = uic.loadUiType("manual_trading.ui")[0]

class ManualTrading(QMainWindow, form_class):
    def __init__(self, kiwoom, connect_state):
        super().__init__()
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

        account_num = int(self.kiwoom.get_login_info("ACCOUNT_CNT"))
        accounts = self.kiwoom.get_login_info("ACCNO")
        accounts_list = accounts.split(';')[0:account_num]
        self.comboBox.addItems(accounts_list)

        self.lineEdit.textChanged.connect(self.code_changed)
        self.pushButton.clicked.connect(self.send_order)
        self.pushButton_2.clicked.connect(self.check_balance)

        self.timer = QTimer(self)
        self.timer.start(1000*10)
        self.timer.timeout.connect(self.timeout)

    def code_changed(self):
        code = self.lineEdit.text()
        name = self.kiwoom.get_master_code_name(code)
        self.lineEdit_2.setText(name)

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

        self.kiwoom.send_order("send_order_req", "0101", account, order_type_lookup[order_type], code, num, price, hoga_lookup[hoga], "")

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

    def timeout(self):
        if self.checkBox.isChecked():
            self.check_balance()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    manual_trading = ManualTrading(0)
    manual_trading.show()
    app.exec_()
    app = None
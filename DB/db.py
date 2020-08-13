import sys
from PyQt5.QtWidgets import *
import DB.DB_Kiwoom as db_kiwoom
from PyQt5.QtTest import *
import time
from pandas import DataFrame
import datetime

class DB:
    def __init__(self):
        self.KOSPI = 0
        self.KOSDAQ = 10

        self.kiwoom = db_kiwoom.DB_Kiwoom()
        self.kiwoom.comm_connect()
        self.get_code_list()

    def get_code_list(self):
        self.kospi_code_list = self.kiwoom.get_code_list_by_market(self.KOSPI)
        self.kosdaq_code_list = self.kiwoom.get_code_list_by_market(self.KOSDAQ)

    def get_ohlcv(self, code, start):

        self.kiwoom.set_input_value("종목코드", code)
        self.kiwoom.set_input_value("기준일자", start)
        self.kiwoom.set_input_value("수정주가구분", 1)
        self.kiwoom.comm_rq_data("주식일봉차트조회요청", "opt10081", 0, "9999")

        QTest.qWait(700)

        df = DataFrame(self.kiwoom.stock_ohlcv, columns=['open', 'high', 'low', 'close', 'volume'],
                       index=self.kiwoom.stock_ohlcv['date'])

        return df

    def check_surge_volume(self, code):
        today = datetime.datetime.today().strftime("%Y%m%d")
        df = self.get_ohlcv(code, today)
        volumes = df['volume']

        if len(volumes) < 21:
            return False

        sum_volume_20 = 0
        today_volume = 0

        for i, volume in enumerate(volumes):
            volume = int(volume)
            if i == 0:
                today_volume = volume
            elif 1 <= i <= 20:
                sum_volume_20 += volume
            else:
                break

        avg_volume_20 = sum_volume_20 / 20

        if today_volume > avg_volume_20 * 10:
            return True

    def update_buy_list(self, buy_list):
        with open("buy_list.txt", "wt") as f:
            for code in buy_list:
                f.writelines("매수;", code, ";시장가;10;0;매수전")

    def run(self):
        buy_list = []
        num = len(self.kosdaq_code_list)

        for i, code in enumerate(self.kospi_code_list):
            print(i, "/", num)
            if self.check_surge_volume(code):
                buy_list.append(code)
                print("발견")

        self.update_buy_list(buy_list)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = DB()
    db.run()
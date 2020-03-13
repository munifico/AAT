"""
QTableWidget 위젯
"""

"""
데이터를 행과 열로 표시.
데이터를 쉽게 파악

QTableWidget 클래스의 인스턴스를 생성하기 위해 생성자를 호출
인자값 = 1. 부모

resize 메서드 크기조절
setRowCount 메서드 = 행의 개수 지정
setColumnCount 메서드 = 열의 개수 지정

2x2 (행x열) 크기의 QTableWidget 객체가 생성되면 (0,0), (0,1), (1,0), (1,1) 위치에 값을 넣을 수 있음.
setItem 메서드로 QTableWidgetItem 객체를 삽입
인자값 = 1. 행에 대한 인덱스, 2. 열에 대한 인덱스, 3. QTableWidgetItem 객체
"""
# import sys
# from PyQt5.QtWidgets import *
#
# class MyWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setupUI()
#
#     def setupUI(self):
#         self. setGeometry(800, 200, 300, 300)
#
#         self.tableWidget = QTableWidget(self)
#         self.tableWidget.resize(290, 290)
#         self.tableWidget.setRowCount(2)
#         self.tableWidget.setColumnCount(2)
#         self.setTableWidgetData()
#
#     def setTableWidgetData(self):
#         self.tableWidget.setItem(0, 0, QTableWidgetItem("(0,0)"))
#         self.tableWidget.setItem(0, 1, QTableWidgetItem("(0,1)"))
#         self.tableWidget.setItem(1, 0, QTableWidgetItem("(1,0)"))
#         self.tableWidget.setItem(1, 1, QTableWidgetItem("(1,1)"))

"""
.setEditTriggers 메서드 -> QTableWidget의 아이템 항목을 수정할 수 없도록 설정
QTableWidget에 아이템을 채우는 코드
column에 대한 라벨 설정.
row 방향에 대한 라벨을 설정할 때는 setVerticalHeaderLabels 메서드 사용 (col 열 / row 행)
(행, 열) 위치에 대한 인덱스를 구하고 해당 위치에 문자열을 넣는 방식으로 구현.
열에 대한 인덱스는 미리 정의된 column_idx_lookup 딕셔너리를 사용.
QTableWidget에 아이템으로 삽입하려면 , 데이터를 QTableWidgetItem 객체로 만들어야 한다.
setItem 메서드를 이용해 아이템을 원하는 위치에 삽입.
종가는 setTextAlignment 메서드를 사용해 우측 정렬
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

kospi_top5 = {
    'code': ['005930', '015760', '005380', '090430', '012330'],
    'name': ['삼성전자', '한국전력', '현대차', '아모레퍼시픽', '현대모비스'],
    'cprice': ['1,269,000', '60,100', '132,000', '414,500', '243,500']
}
column_idx_lookup = {'code': 0, 'name': 1, 'cprice': 2}

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(290, 290)
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setTableWidgetData()

    def setTableWidgetData(self):
        column_header = ['종목코드', '종목명', '종가']
        self.tableWidget.setHorizontalHeaderLabels(column_header)

        for k, v in kospi_top5.items():
            col = column_idx_lookup[k]
            for row, val in enumerate(v):
                item = QTableWidgetItem(val)
                if col == 2:
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

                self.tableWidget.setItem(row, col, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
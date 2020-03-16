"""
matplotlib을 이용해 PyQt 내에 그래프 그리기
"""

"""
matplotlib을 이용해 PyQt 내에 그래프 그리려면.
FigureCanvasQTAgg 클래스 사용

FigureCanvas 객체 생성
인자값 plt.Figure()

객체를 상단으로 배치하기 위해 addStrestch 메서드 호출
addStrestch 메서드는 크기 조절이 가능한 공백 추가

메인 윈도우의 크기가 변경될 때
그래프가 출력되는 leftLayout만 크기 조절이 가능하도록 설정.
인자값 1. 레이아웃 2. 비율
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(600, 200, 1200, 600)
        self.setWindowTitle("PyChart")
        self.setWindowIcon(QIcon('icon.png'))

        self.lineEdit = QLineEdit()
        self.pushButton = QPushButton("차트그리기")
        self.pushButton.clicked.connect(self.pushButtonClicked)

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.canvas)

        rightLayout = QVBoxLayout()
        rightLayout.addStretch(3)
        rightLayout.addWidget(self.lineEdit)
        rightLayout.addWidget(self.pushButton)
        rightLayout.addStretch(1)

        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        layout.setStretchFactor(leftLayout, 1)
        layout.setStretchFactor(rightLayout, 1)

        self.setLayout(layout)

    def pushButtonClicked(self):
        print(self.lineEdit.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()

"""
FigureCanvas 객체에 그래프를 그리기 위해 .draw() 메서드 호출
"""
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# import pandas_datareader.data as web
# import pandas as pd
# from pandas import Series, DataFrame
#
# class MyWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setupUI()
#
#     def setupUI(self):
#         self.setGeometry(600, 200, 1200, 600)
#         self.setWindowTitle("PyChart Viewer v0.1")
#         self.setWindowIcon(QIcon('icon.png'))
#
#         self.lineEdit = QLineEdit()
#         self.pushButton = QPushButton("차트그리기")
#         self.pushButton.clicked.connect(self.pushButtonClicked)
#
#         self.fig = plt.Figure()
#         self.canvas = FigureCanvas(self.fig)
#
#         leftLayout = QVBoxLayout()
#         leftLayout.addWidget(self.canvas)
#
#         # Right Layout
#         rightLayout = QVBoxLayout()
#         rightLayout.addWidget(self.lineEdit)
#         rightLayout.addWidget(self.pushButton)
#         rightLayout.addStretch(1)
#
#         layout = QHBoxLayout()
#         layout.addLayout(leftLayout)
#         layout.addLayout(rightLayout)
#         layout.setStretchFactor(leftLayout, 1)
#         layout.setStretchFactor(rightLayout, 0)
#
#         self.setLayout(layout)
#
#     def pushButtonClicked(self):
#         code = self.lineEdit.text()
#         df = web.DataReader(code + ".ks", "yahoo")
#         df['MA20'] = df['Adj Close'].rolling(window=20).mean()
#         df['MA60'] = df['Adj Close'].rolling(window=60).mean()
#
#         ax = self.fig.add_subplot(111)
#         ax.plot(df.index, df['Adj Close'], label='Adj Close')
#         ax.plot(df.index, df['MA20'], label='MA20')
#         ax.plot(df.index, df['MA60'], label='MA60')
#         ax.legend(loc='upper right')
#         ax.grid()
#
#         self.canvas.draw()
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     app.exec_()
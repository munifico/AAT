import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")

        self.setWindowTitle("종목 코드")
        self.setGeometry(300, 300, 300, 150)

        btn1 = QPushButton("종목코드 얻기", self)
        btn1.move(190, 10)
        btn1.clicked.connect(self.btn1_clicked)

        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(10, 10, 170, 130)
    """
    GetCodeListByMarket 메서드
    종목 코드를 가져오는 메서드
    원형 = BSTR GetCodeListByMarket(LPCTSTR sMarket)
    인자 (sMarket) = 0:장내, 3:ELW, 4:뮤추얼펀드, 5:신주인수권, 6:리츠, 
                    8:ETF, 9:하이일드펀드, 10:코스닥, 30:K-OTC, 50:코넥스(KONEX)
    반환 = 해당 시장에 속한 종목의 종목 코드 목록.
    
    GetMasterCodeName 메서드
    종목 코드로부터 한글 종목명을 반환
    원형 = BSTR GetMasterCodeName(LPCTSTR strCode)
    인자 = 종목 코드
    반환 = 종목한글명
    """
    def btn1_clicked(self):
        ret = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)",["0"])
        kospi_code_list = ret.split(';')
        kospi_code_name_list = []
        print(kospi_code_list)
        for x in kospi_code_list:
            name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)",[x])
            kospi_code_name_list.append(x + " : " + name)

        self.listWidget.addItems(kospi_code_name_list)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())
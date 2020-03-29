import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        print("create kiwoom")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        print("signal_slots")

    def comm_connect(self):
        print("comm_connect")
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()


    def _event_connect(self, err_code):
        if err_code == 0:
            print("connect")
        else:
            print("disconnect")

        self.login_event_loop.exit()

    def get_connect_state(self):
        result = self.dynamicCall("GetConnectState()")
        return result

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.show()
    kiwoom.comm_connect()
    app.exec_()
    app = None
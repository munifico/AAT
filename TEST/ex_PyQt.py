"""
GUI 프로그래밍

알고리즘 트레이딩을 하는 데 GUI 프로그래밍이 꼭 필요한 것은 아닙니다.
GUI나 TUI(Text-based User Interface)는 데이터를 효과적으로 표현하기 위한 수단일 뿐 프로그램의 핵심 로직이나 알고리즘과는 관계가 없기 때문입니다.
그렇지만 여러분이 자주 사용하는 HTS가 텍스트 기반으로 동작한다면 조금 불편하겠지요?
이번 장을 통해 PyQt를 제대로 배워둔다면 여러분들이 만들려는 프로그램을 쉽게 개발할 수 있을 것입니다.

PyQt는 파이썬에서 GUI 프로그래밍을 할 때 사용하는 대표적인 패키지
Anaconda에서는 PyQt5 버전이 기본 패키지
"""

"""
PyQt 기반의 GUI 프로그램의 핵심 구성 요소는.
화면에 출력되는 UI부분, -> PyQt가 기본적으로 제공하는 위젯(Widget) 클래스의 객체를 생성해서 만듬
이벤트 루프 -> QApplication 객체에서 exec_ 메서드를 호출해 이벤트 루프를 생성.
이벤트를 처리할 함수 또는 메서드 구현 -> 버튼 위젯을 클릭하면 'clicked'라는 시그널(signal)을 발생. 
                                        -> 'clicked'라는 시그널이 발생했을 때 호출되는 함수 또는 메서드를 구현해야함.
                                    PyQt에서는 특정 시그널이 발생했을 때 호출되는 함수 또는 메서드를 슬롯(slot)이라 함.
                                    다른 프로그래밍 언어에서즌 콜백 함수(callback function)라고 부름
PyQt에서는
위젯에서 발생하는 시그널에 대해 어떤 슬롯으로 처리할지에 대해 미리 등록함으로써
특정 위젯에서 시그널이 발생했을 때 이벤트 루프가 미리 연결된 슬롯을 자동으로 호출.

사용자가 버튼 위젯 클릭 -> clicked 시그널 발생
-> GUI 프로그램의 시작과 함께 생성돼 있던 이벤트 루프 -> 시그널에 등록된 슬롯을 호출해서 사용자가 발생시킨 이벤트 처리

이벤트 루프는 사용자가 프로그램을 종료한다는 시그널을 보내기 전까지 위 방식으로 시그널과 연결된 슬롯을 호출함으로써 이벤트 처리
"""

"""
이벤트 루프는 QApplication 클래스의 객체를 생성한 후 exec_ 메서드를 호출하는 순간 생성.
생성된 이벤트 루프는 사용자가 윈도우를 닫을 때까지 실행되면서 위젯에서 발생한 시그널을 처리하는 슬롯을 호출.

파이썬 코드는 파일 위에서부터 아래로 순차적으로 실행.
app.exec_() 다음 줄 코드는 실행되지 않았다.
= 이벤트 루프가 생성됐고 -> 프로그램이 계속해서 이벤트 루프 안에서 실행되고 있기 때문.
"""
# import sys
# from PyQt5.QtWidgets import *
#
# app = QApplication(sys.argv)
# label = QLabel("Hello, PyQt")
# label.show()
#
# print("Before event loop")
# app.exec_()
# print("After event loop")

"""
PyQt는 위젯의 종류에 따라 발생 가능한 기본 시그널이 정의돼 있다.

시그널이 발생했을 때 호출되는 함수 또는 메서드를 슬롯이라 부른다.
슬롯을 구현하고 시그널과 슬롯을 연결해주면 된다.
시그널이 발생했을 때 연결된 슬롯을 호출하는 역할은 이벤트 루프가 알아서 처리.

슬롯의 구현과 시그널-슬롯의 연결이 모두 이벤트 루프를 생성하는 app.exec_ 메서드 호출보다 먼저 수행되야 함.
"""
# import sys
# from PyQt5.QtWidgets import *
#
# def clicked_slot():
#     print('clicked')
#
# app = QApplication(sys.argv)
#
# btn = QPushButton("Hello, PyQt")
# btn.clicked.connect(clicked_slot)
# btn.show()
#
# app.exec_()

"""
PyQt에서 위젯은 UI를 구성하는 핵심 요소다.
PyQt에서는 모든 위젯이 최상위 위젯을 의미하는 윈도우가 될 수 있다.
그러나 대부분의 프로그램에서는 QMainWindow나 QDialog 클래스를 사용해 윈도우를 생성.

QApplication 객체인 app을 생성하고 exec_ 메서드를 호출해서 이벤트 루프를 생성.
이벤트 루프를 생성하기 전에 MyWindow라는 클래스 객체를 생성 -> 이벤트 루프를 생성하기 전에 UI를 구성
-> UI를 구성하는 기본 단위인 위젯에 대해 시그널과 슬롯을 연결해야 한다.

UI가 복잡한 경우 클래스 사용 추천.
클래스를 사용하면 상속 활용 가능

MyWindow 클래스의 객체는 이벤트 루프가 실행되기 전에 생성, 자동으로 생성자 호출.
-> 생성자부터 보기.

QPushButton 같은 객체 생성 코드를 따로 메서드로 구성해서 코드의 가독성을 높인다.

btn1.clicked.connect(self.btn1_clicked)는
clicked라는 시그널과 self.btn1_clicked 슬롯을 연결하는 코드
"""
import sys
from PyQt5.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Review")

        btn1 = QPushButton("click me", self)
        btn1.move(20, 20)
        btn1.clicked.connect(self.btn1_clicked)

    def btn1_clicked(self):
        QMessageBox.about(self, "message", "clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()



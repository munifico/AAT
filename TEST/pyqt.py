import sys
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)    # QApplication 클래스  # sys.argv 현재 소스코드에 대한 절대 경로
                                                    # QApplication 클래스의 인스턴스를 생성할때 생성자에 이 값 전달
label = QLabel("Hello PyQt")    # QLabel 클래스
label.show()                    # QLabel 클래스의 show 메서드
label2 = QPushButton("Quit")    # QPushButton 클래스
label2.show()                   # QPushButton 클래스의 show 메서드
print(sys.argv)
app.exec_() # app을 통해 exec_를 호출하면 이벤트 루프에 진입
            # 이벤트 루프 = 무한 반복하면서 이벤트를 처리하는 상태
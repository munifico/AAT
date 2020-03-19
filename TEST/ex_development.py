"""
PyTrader
키움 Open API+ 를 이용한 자동 로그인을 지원.
PyQt를 통해 개발.
상태 표시줄에 현재 시각과 키움증권 연결 여부를 매초 출력

윈도우 작업 스케줄러를 이용해 PyTrader 프로그램을 정해진 시간에 자동으로 실행되게 할 것.
키움 증권의 버전 처리를 자동으로 수행하기 위해 번개 3를 자동으로 로그인하고 종료하는 파이썬 스크립트 작성
"""

"""
키움 OpenAPI+도 하나의 프로그램.
주기적으로 업데이트
PC에 설치된 키움 OpenAPI+ 모듈을 업데이트 해야함.
키움증권에서는 이러한 과정을 버전 처리라고 함.

버전 처리를 쉽게하는 방법은 OpenAPI+를 사용하기 위해 설치했던 번개 HTS를 사용하는 것.
번개 HTS를 실행하면 자동으로 버전 처리가 완료되기 때문.

pywinauto 패키지
윈도우 대화상자에 자동으로 마우스나 키보드 이벤트를 보낼 수 있다.
윈도우 대화상자의 이름과 각 컨트롤의 이름을 알아내기 위해 SWAPY를 사용한다.
윈도우 상에 실행 중인 프로그램의 구조를 살펴볼 수 있다.

키움 번개3을 실행하는 코드가 포함되어 있어서 IDE도 관리자 권한으로 실행해야함.

번개3은 버전 처리를 위해 실행한 프로그램.
실 거래는 OpenAPI+를 통해 개발한 프로그램에서 처리.
따라서 번개 3은 종료해야함.

윈도우에서는 taskkill 명령을 통해 특정 프로그램을 종료할 수 있다.
윈도우 명령을 사용하려면 os 모듈의 system 함수를 사용해야한다.

코드를 완성했다면 윈도우 작업 스케줄러를 사용해서 자동화를 시켜줘야 한다.

"""

from pywinauto import application
from pywinauto import timings
import time
import os

app = application.Application()
app.start("C:/KiwoomFlash3/Bin/NKMiniStarter.exe")

title = "번개3 Login"
dlg = timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title=title))

pass_ctrl = dlg.Edit2
pass_ctrl.SetFocus()
pass_ctrl.TypeKeys('1234')

cert_ctrl = dlg.Edit3
cert_ctrl.SetFocus()
cert_ctrl.TypeKeys('1234')

btn_ctrl = dlg.Button0
btn_ctrl.Click()

time.sleep(60)
os.system("taskkill /im NKMini.exe")
from pywinauto import application
from pywinauto import timings
import time
import os

SECU_BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),"security_file")

app = application.Application()
app.start("C:/KiwoomFlash3/Bin/NKMiniStarter.exe")

title = "번개3 Login"
dlg = timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title=title))

with open(os.path.join(SECU_BASE_DIR, "top_security2.txt"), 'r+', encoding='utf-8') as f_read:
    service_key = f_read.readline().split(',')

print(service_key)
password = service_key[0]
super_password = service_key[1]



pass_ctrl = dlg.Edit2
pass_ctrl.SetFocus()
pass_ctrl.TypeKeys(password)

cert_ctrl = dlg.Edit3
cert_ctrl.SetFocus()
cert_ctrl.TypeKeys(super_password)

btn_ctrl = dlg.Button0
btn_ctrl.Click()

time.sleep(300)
os.system("taskkill /im NKMini.exe")
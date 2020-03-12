"""
pie 차트를 원형 차트라고 부른다.

pie 차트는 각 범주가 데이터에서 차지하는 비율을 나타내는 데 자주 사용.

"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager,rc
from matplotlib import style

"""
ggplot은 스타일의 한 종류.
matplotlib은 ggplot 외에도 여러 가지 스타일을 제공
"""
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
style.use('ggplot')

labels = ['삼성전자', 'SK하이닉스', 'LG전자', '네이버', '카카오']
ratio = [50, 20, 10, 10, 10]

"""
pie 차트는 matplotlib.pyplot 모듈의 pie 함수를 사용해 그릴 수 있다. 

명시적으로 Figure, AxesSubplot 객체를 생성하지 않았다.
명시적으로 객체를 생성하지 않아도 matplotlib.pyplot 모듈의 그래프 출력 함수가 호출될 때 자동으로 객체가 생성.

pie 함수의 첫 번째 인자는 각 범주가 데이터에서 차지하는 비율.
두 번째 인자는 범주
shadow는 차트에 그림자 설정
startangle = 첫 번째 pie의 시작 각도. / pie 차트를 4사분면으로 나눠서 +x축이 0도
"""
plt.pie(ratio, labels=labels, shadow=True, startangle=110)
plt.show()

"""
특정 pie를 확대하려면 각 범주에 확대 값을 리스트 형태로 전달.
각 범주가 데이터에서 차지하는 비율을 출력하기 위해 autopct 키워드 인자를 사용.
"""
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'red']
explode = (0.0, 0.1, 0.0, 0.0, 0.0)

plt.pie(ratio, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
plt.show()

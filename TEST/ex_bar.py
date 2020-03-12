"""
bar 차트는 막대그래프라고 한다.

bar 차트는 데이터를 분류한 후 각 데이터를 비교하는데 많이 사용.
"""

"""
font_manager, rc 모듈은 그래프를 그릴 때 한글 폰트를 설정하는 데 사용
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager, rc

font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

"""
다음 금융 -> 업종명 데이터
"""
industry = ['통신업', '의료정밀', '운수창고업', '의약품', '음식료품', '전기가스업', '서비스업', '전기전자', '종이목재', '증권']
fluctuations = [1.83, 1.30, 1.30, 1.26, 1.06, 0.93, 0.77, 0.68, 0.65, 0.61]

"""
Figure 객체, AxesSubplot 객체
"""
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)

"""
수평 방향의 bar 차트는 matplotlib.pyplot 모듈의 barh 함수를 사용해 그린다.
barh 함수의 첫 번째 인자는 각 bar가 그려질 위치
두 번째 인자는 각 bar에 대한 수치
위 둘은 파이썬 리스트 형식으로 전달
align은 bar 차트에서 bar의 정렬 위치
height는 수평 bar 차트의 높이

수평 방향의 bar 차트에서는 y축에 ticker를 표시.
matplotlib.pyplot 모듈의 yticks 함수를 사용해 ticker의 위치와 각 위치에서의 label을 설정
"""
ypos = np.arange(10)
rects = plt.barh(ypos, fluctuations, align='center', height=0.5)
plt.yticks(ypos, industry)
#
# plt.xlabel('등락률')
# plt.show()

"""
수치 값이 bar 차트에 출력되도록 설정.
스타일을 변경하려면 matplotlib.style 모듈을 임포트 하고 style을 설정.
그래프의 style을 변경하는 코드는 그래프를 출력(plt.show 함수 호출)하기 전에 수행해야 한다.
"""
from matplotlib import style

style.use('ggplot')

"""
bar 차트의 각 bar에 등락률 데이터를 출력.
.text 함수 사용.
첫 번째 인자는 text가 출력되는 x축 위치
두 번째 인자는 text가 출력될 y축 위치
세 번째는 실제로 표시될 값을 전달
ha는 수평 방향으로의 정렬
va는 수직 방향으로의 정렬

첫 번째 인자에 rect.get_width를 사용 / rect는 bar 차트에서 각 bar에 해당
각 bar의 너비(길이)를 알아낸 후 그 너비의 95% 지점이 텍스트가 출력될 x축 위치
두 번째 인자는 bar가 출력된 y축 위치를 rect.get_y를 통해 얻고 bar 높이의 절반을 더함으로써 y축 위치 계산
"""
for i, rect in enumerate(rects):
    ax.text(0.95 * rect.get_width(), rect.get_y() + rect.get_height() / 2.0, str(fluctuations[i]) + '%', ha='right', va='center')

plt.xlabel('등락률')
plt.show()

"""
수직 방향 bar 차트
matplotlib.pyplot 모듈의 bar 함수를 사용.
"""
pos = np.arange(10)
rects = plt.bar(pos, fluctuations, align='center', width=0.5)
plt.xticks(pos, industry)

for i, rect in enumerate(rects):
    ax.text(rect.get_x() + rect.get_width() / 2.0, 0.95 * rect.get_height(), str(fluctuations[i]) + '%', ha='center')

plt.ylabel('등락률')
plt.show()
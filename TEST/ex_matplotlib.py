"""
데이터 시각화

파이썬은 데이터 시각화를 위해 다양한 라이브러리를 제공

matplotlib은 파이썬에서 2차원 그래프를 그릴 때 가장 널리 사용.
"""

"""
pyplot
Mathworks에서 개발
공학이나 과학 분야에서 주로 사용되는 프로그래밍 언어로 매트랩(MATLAB)이 있다.
매트랩은 공학 및 과학 문제 해결에 최적화된 프로그래밍 환경으로서 다양한 분야에서 활용.

matplotlib의 pyplot 모듈은 매트랩과 비슷한 형태로 그래프를 그리는 기능을 제공.

"""
"""
y축 값 1, 2, 3, 4를 지나는 직선.
x 축 값을 따로 지정하지 않으면 자동으로 실수값이 할당.
"""
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4])
# plt.show()
"""
x축 값과 y축 값을 동시에 받을 수 있다.
첫 y는 리스트 내장이다.

"""
x = range(0, 100)
y = [v*v for v in x]
y = []
for v in x:
    y.append(v*v)

plt.plot(x, y)
# plt.show()
"""
plot 함수로 그래프의 색, 형태도 변경가능.
기본 포맷은 파란색 직선(b-)이다. 빨간색 원(ro)

표 15.1 matplotlib의 주요 색상

문자	색상
b	blue(파란색)
g	green(녹색)
r	red(빨간색)
c	cyan(청록색)
m	magenta(마젠타색)
y	yellow(노란색)
k	black(검은색)
w	white(흰색)
matplotlib에서 자주 사용되는 마커는 표 15.2와 같습니다.

표 15.2 matplotlib의 주요 마커

마커	의미
o	circle(원)
v	triangle_down(역 삼각형)
^	triangle_up(삼각형)
s	square(네모)
+	plus(플러스)
.	point(점)
"""
x = range(0, 100)
y = [v*v for v in x]
plt.plot(x, y, 'ro')
# plt.show()
"""
한 화면에 여러 개의 그래프를 그리는 방법

한 화면에 여러 개의 그래프를 그리려면 figure 함수를 통해 Figure 객체를 만든 후
add_subplot 메서드를 통해 그리려는 그래프 수 만큼 subplot을 만듦

subplot의 개수는 add_subplot 메서드의 인자를 통해 조정.
(2, 1, 1)은 2x1(행x열)의 subplot을 생성. 세 번째 인자 1은 생성된 subplot 중 첫 번째 subplot을 의미

add_subplot 메서드를 호출하면 AxesSubplot 객체가 생성.
Axes는 하나의 subplot과 유사한 개념
"""
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
# plt.show()
"""
첫 번째 subplot에는 plot 함수를 호출해서 그래프를 그림
두 번째 subplot에는 bar 함수를 호출해서 그래프를 그림 막대 그래프 그릴 때 사용
"""
import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

x = range(0, 100)
y = [v*v for v in x]

ax1.plot(x,y)
ax2.bar(x,y)

plt.show()
"""
0-2pi 범위의 sin, cos 그래프
x의 값이 실수 범위라 range대신 numpy 모듈의 arange를 사용

"""
import numpy as np
import matplotlib.pyplot as plt2

x = np.arange(0.0, 2 * np.pi, 0.1)
sin_y = np.sin(x)
cos_y = np.cos(x)

fig = plt2.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

ax1.plot(x, sin_y, 'b--')
ax2.plot(x, cos_y, 'r--')

plt2.show()

import numpy as np
import matplotlib.pyplot as plt2

x = np.arange(0.0, 2 * np.pi, 0.1)
sin_y = np.sin(x)
cos_y = np.cos(x)

plt2.plot(x, sin_y, 'b--')
plt2.plot(x, cos_y, 'r--')

plt2.show()

"""
subplot은 Axes 객체.
Axes 객체는 set_xlabel, set_ylabel 메서드를 통해 x축과 y축에 라벨을 설정.
"""
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0.0, 2 * np.pi, 0.1)
sin_y = np.sin(x)
cos_y = np.cos(x)

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)


ax1.plot(x, sin_y, 'b--')
ax2.plot(x, cos_y, 'r--')

ax1.set_xlabel('x')
ax1.set_ylabel('sin(x)')

ax2.set_xlabel('x')
ax2.set_ylabel('cos(x)')

plt.show()

"""
plot 함수에 label= 인자를 통해 라벨을 지정.
label을 통해 전달하는 문자열이 범례에 표시

범례는 legend 함수를 통해 추가.
loc 인자로 범례 표시 위치를 지정.

표 15.3 legend loc 파라미터 옵션

Location String	Location Code
‘best’	0
‘upper right’	1
‘upper left’	2
‘lower left’	3
‘lower right’	4
‘right’	5
‘center left’	6
‘center right’	7
‘lower center’	8
‘upper center’	9
‘center’	10
"""
import pandas_datareader.data as web
import matplotlib.pyplot as plt

lg = web.DataReader("066570.KS", "yahoo")
samsung = web.DataReader("005930.KS", "yahoo")

plt.plot(lg.index, lg['Adj Close'], label='LG Electronics')

plt.legend(loc='upper left')

plt.show()

"""
matplotlib의 Figure 객체의 구성.
matplotlib로 그래프를 그리려면 Figure 객체와 하나 이상의 subplot(Axes) 객체가 필요.
Axes 객체는 다시 두 개의 Axis 객체를 포함.
Axis 객체는 x축, y축

matplotlib에서 그래프는 Figure 객체 내에 존재.
그래프를 그리려면 figure 함수를 사용해 Figure 객체를 생성
"""
import matplotlib.pyplot as plt

fig = plt.figure()

print(type(fig))    # <class 'matplotlib.figure.Figure'>

ax = fig.add_subplot(1, 1, 1)

print(type(ax))     # <class 'matplotlib.axes._subplots.AxesSubplot'>

plt.show()

"""
plt.show()는 생성된 Figure 객체를 전부 show()
"""

"""
Figure 객체를 생성. 해당 Figure 객체에 여러 개의 AxesSubplot 객체를 생성하는 두 가지 작업을 한번에 하려면.
plt.subplots를 사용.
plt.subplots(2,2)는 Figure 객체와 2x2 그리드 형태의 AxesSubplot 객체가 생성
"""
fig, ax_list = plt.subplots(2, 2)

print(ax_list)
# [[<matplotlib.axes._subplots.AxesSubplot object at 0x07952C70>
#   <matplotlib.axes._subplots.AxesSubplot object at 0x07798550>]
#  [<matplotlib.axes._subplots.AxesSubplot object at 0x0BDEBBD0>
#   <matplotlib.axes._subplots.AxesSubplot object at 0x0BDD1250>]]

ax_list[0][0].plot([1, 2, 3, 4])

plt.show()

"""
Figure 객체나 AxesSubplot 객체를 명시적으로 생성하지 않고도 plt.plot 함수를 통해 그래프를 그렸다.
plt.plot 함수가 자동으로 가장 최근에 생성된 Figure 객체를 찾고 해당 Figure 객체 내의 AxesSubplot에 그래프를 그리기 때문.
Figure와 AxesSubplot 객체가 없다면 Figure 객체와 AxesSubplot를 하나 생성.
그래서 Figure와 AxesSubplot 객체를 명시적으로 만들지 않고도 그래프를 그릴 수 있었음.
"""

###

"""
그래프를 그리는 데 matplotlib 라이브러리의 pyplot 모듈 사용
Figure 객체와 AxesSubplot 객체를 만든 후 plot 함수를 사용해 그래프를 그림.
AxesSubplot 객체를 만들 때 add_subplot이 아닌 subplot2grid 함수를 사용했다는 점이 다름.
"""
import matplotlib.pyplot as plt
import pandas_datareader.data as web

sk_hynix = web.DataReader("000660.KS", "yahoo")

fig = plt.figure(figsize=(12, 8))

top_axes = plt.subplot2grid((4,4), (0,0), rowspan=3, colspan=4)
bottom_axes = plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=4)
bottom_axes.get_yaxis().get_major_formatter().set_scientific(False)

top_axes.plot(sk_hynix.index, sk_hynix['Adj Close'], label='Adjusted Close')
bottom_axes.plot(sk_hynix.index, sk_hynix['Volume'])

plt.tight_layout()
plt.show()

"""
Figure 객체와 크기가 서로 다른 두 개의 AxesSubplot 객체를 생성하는 코드만 실행.
Figure 객체에 크기가 다른 두 개의 AxesSubplots 객체가 생성

Figure 객체를 생성하는 코드에 figsize라는 인자를 통해 Figure 객체의 크기를 조정.
일반적으로 주식 데이터를 그래프로 그릴 때는 높이보다 너비를 조금 더 길게 설정하는 것이 보기 편리.

AxesSubplot 객체는 add_subplot이나 subplots를 사용하지 않고 subplot2grid를 사용.
subplot2grid는 subplot의 위치나 크기를 조절할 때 사용

subplot2grid 함수에서 첫 번째 인자인 (4,4)는 4x4 grid 모양을 의미
두 번째 인자인 (0,0)은 4x4 grid에서 (0,0)에 위치하는 grid를 의미
세 번째 인자인 rowspan = 3 은 gird가 행 방향으로 3개만큼 걸치는 것을 의미.
네 번째 인자인 colspan = 4 는 grid가 열 방향으로 4개만큼 걸치는 것을 의미.

두 번째로 호출되는 subplot2grid 함수에서
첫 번째 인자는 (4,4)로 4x4 grid를 의미
두 번째 인자는 (3,0)은 4x4 grid에서 (3,0)에 위치하는 grid를 의미
세 번째 인자 rowspan = 1 은 행 방향으로 1개
네 번째 인자 colspan = 1 은 열 방향으로 4개

거래량 그래프가 출력되는 bottom_axes라는 AxesSubplot 객체는.
거래량 값으로 큰 값이 발생할 때 그 값을 오일러 상수(e)의 지수 형태로 표현되지 않게 해줌.

tight_layout 함수는 subplot들이 Figure 객체의 영역 내에서 자동으로 최대 크기로 출력.
"""
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(12, 8))

top_axes = plt.subplot2grid((4,4), (0,0), rowspan=3, colspan=4)
bottom_axes = plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=4)

bottom_axes.get_yaxis().get_major_formatter().set_scientific(False)

plt.show()



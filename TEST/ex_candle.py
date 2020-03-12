"""
캔들 스틱 차트

matplotlib에서 캔들 스틱 차트를 그리는 함수 이름 = candle로 시작
국내에서는 캔들보다는 봉 차트라고 부름

일봉
거래일 동안의 시가, 고가, 저가, 종가의 네 가지 값을 한 개의 봉으로 표현
일봉 중 종가가 시가보다 높은 경우를 양봉
종가가 시가보다 낮은 경우를 음봉
양봉은 빨간색, 음봉은 파란색.

봉 차트에서는 시가, 고가, 종가, 저가 네 가지 값으로 해당 거래일의 추가 추이를 나타낸다.
종가와 고가 사이의 간격이 큰 것은 하루 중 주가가 크게 올랐다 떨어짐을 의미.

봉 차트에서는 시가와 종가 사이를 몸통이라 부름.
몸통 윗부분을 머리.
몸통 아래를 꼬리라고 부름.
봉을 그릴 때 몸통은 두껍게, 고가와, 저가를 나타내는 머리, 꼬리는 얇은 실선으로 표시

투자 책에서는 약세시점에서 양봉 3개가 나타나는 것을 '적삼병'이라 부르고 이를 주가 상승 장세의 시점으로 봄.
반대로 상승 시점에서 음봉 3개가 연달아 나타나면 이를 '흑삼병' 하락 시점으로 봄
"""
import pandas_datareader.data as web
import datetime

start = datetime.datetime(2016, 3, 1)
end = datetime.datetime(2016, 3, 31)

skhynix = web.DataReader("000660.KS", "yahoo", start, end)

"""
실험중

mpl_finance 20년 중순쯤 지원이 중단된다고 함.
최신 버전은 mplfinance 인데
mplfinance는 matplotlib.pyplot가 동시에 지원됨.
mpf.plot을 사용하면 봉 그래프가 나옴

기존 봉 그래프를 사용하려면 mplfinance.original_flavor 를 사용하면 됨.
candlestick2_ohlc 같은 메소드
"""
# import mpl_finance
# # 밑에 두개가 최신 지원 버전
# import mplfinance as mpf
# import mplfinance.original_flavor as mpl
# import matplotlib.pyplot as plt
#
# mpf.plot(skhynix)
#
# # fig = plt.figure(figsize=(12,8))
# # ax = fig.add_subplot(211)
# #
# # fig1 = plt.figure(figsize=(12,8))
# # # add_subplot 뭐냐
# # ax1 = fig1.add_subplot(212)
#
# fig = plt.figure(figsize=(12,8))
# ax = fig.add_subplot(111)
#
# fig1 = plt.figure(figsize=(12,8))
# # add_subplot 뭐냐
# ax1 = fig1.add_subplot(111)
#
#
# # 잘됨 판다만 고치면 될듯
# # 고쳤다.
# # C:/Anaconda3/Lib/site-packages/pandas_datareader/compat/__init__.py:8: FutureWarning: pandas.util.testing is deprecated. Use the functions in the public API at pandas.testing instead.
# #   from pandas.util.testing import assert_frame_equal
# # -> from pandas.testing import assert_frame_equal
#
# # 둘 중 한개만 실행되는 듯
# # 두 개 같은 동작
#
# mpl_finance.candlestick2_ohlc(ax, skhynix['Open'], skhynix['High'], skhynix['Low'], skhynix['Close'], width=0.5, colorup='r', colordown='b')
#
# # plt.show()
#
# mpl.candlestick2_ohlc(ax1, skhynix['Open'], skhynix['High'], skhynix['Low'], skhynix['Close'], width=0.5, colorup='r', colordown='b')
#
# plt.show()

"""
봉 차트는 mpl_finance 모듈의 candlestick2_ohlc 함수를 이용하면 그릴 수 있다.

Figure 객체와 AxesSubplot 객체를 만든 후 candlestick2_ohlc 함수를 호출.
mpl_finance 모듈의 candlestick2_ohlc 함수 호출 부분을 살펴보면
첫 번째 인자로 AxesSubplot 객체가 사용.
두 번째 부터 다섯 번째 인자는 시가, 고가, 저가, 종가.
width= 봉의 몸통의 너비 조절
colorup = 양봉 색
colordown = 음봉 색
"""
import pandas_datareader.data as web
import datetime
import mpl_finance
import matplotlib.pyplot as plt

start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 1, 31)

skhynix = web.DataReader("000660.KS", "yahoo", start, end)
skhynix = skhynix[skhynix['Volume'] > 0]

fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)

# mpl_finance.candlestick2_ohlc(ax, skhynix['Open'], skhynix['High'], skhynix['Low'], skhynix['Close'], width=0.5, colorup='r', colordown='b')
#
# plt.show()

"""
DataReader 함수를 통해 얻어온 DataFrame 객체에는 날짜 정보가 저장돼 있다.

.index는 DataFrame 객체 날짜 정보가 저장.
객체 타입은 <class 'pandas.core.indexes.datetimes.DatetimeIndex'>
.index[0]은 2020-01-02 00:00:00 이 저장
객체 타입은 <class 'pandas._libs.tslibs.timestamps.Timestamp'>
"""
print(skhynix.index)
print(type(skhynix.index))

print(skhynix.index[0])
print((type(skhynix.index[0])))

"""
Pandas의 Timestamp 객체는 strtime 메서드에 출력 포멧을 전달해서 문자열로 변환 가능.
%Y-%m-%d
"""
print(skhynix.index[0].strftime('%d'))
print(skhynix.index[0].strftime('%y-%m-%d'))
"""
필요한 값을 빈 리스트에 추가
"""
name_list = []

for day in skhynix.index:
    name_list.append(day.strftime('%d'))

day_list = range(len(skhynix))
print('\n')
print(name_list)
print(day_list)
"""
matplotlib에서 x축과 y축에 표시되는 값을 ticker라고 부른다.
ticker를 설정하려면 ticker의 위치와 위치에서 출력될 값이 필요하다.

x축은 날짜를 의미한다.
날짜 값은 준비돼 있으므로 위치에는 일정하게 증가하는 정숫값을 사용.

x축 ticker의 위치, 위치에서 출력될 값이 전부 준비됨.

x축의 위치와 출력 값을 설정.
위치를 설정하는 함수 set_major_locator
출력되는 값을 설정하는 함수 set_major_formatter

matplotlib.ticker 모듈을 임포트 한 후 x축에 대해서만 설정.
set_major_locator, set_major_formatter 함수에 인자를 전달 할 때
ticker.FixedLocator, ticker.FixedFormatter를 사용
각각 고정 위치와 고정된 포매팅이라는 것을 의미
"""
import matplotlib.ticker as ticker
import numpy as np

ax.xaxis.set_major_locator(ticker.FixedLocator(day_list))
ax.xaxis.set_major_formatter(ticker.FixedFormatter(name_list))

plt.xticks(day_list, name_list)

mpl_finance.candlestick2_ohlc(ax, skhynix['Open'], skhynix['High'], skhynix['Low'], skhynix['Close'], width=0.5, colorup='r', colordown='b')

plt.show()

"""
x축에 각 날짜를 모두 표시하지 않고 매주 월요일에만 '년-월-일' 포맷으로 출력.

Timestamp 객체에는 dayofweek라는 속성이 있다.
속성을 사용하면 거래일의 요일을 쉽게 확인할 수 있다.
0 - 6 월 - 일
"""
day_list = []
name_list = []

for i, day in enumerate(skhynix.index):
    if day.dayofweek == 0:
        day_list.append(i)
        name_list.append(day.strftime('%Y-%m-%d') + '(Mon)')

print(day_list)
print(name_list)

ax.xaxis.set_major_formatter(ticker.FixedFormatter(name_list))
ax.xaxis.set_major_locator(ticker.FixedLocator(day_list))

mpl_finance.candlestick2_ohlc(ax, skhynix['Open'], skhynix['High'], skhynix['Low'], skhynix['Close'], width=0.5, colorup='r', colordown='b')
plt.grid()
plt.show()


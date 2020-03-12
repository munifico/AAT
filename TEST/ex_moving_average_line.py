"""
이동평균선
일정 기간 동안의 주가를 산술 평균한 값인 주가이동평균을 차례로 연결해 만든 선

5일 이평선은 주가 이동 평균 계산일을 기준으로 최근 5일 수정 종가의 평균.
"""
import pandas as pd
import pandas_datareader.data as web

gs = web.DataReader("078930.KS", "yahoo", "2014-01-01", "2020-03-02")

print(gs.tail())
"""
ma5의 타입은 pandas.core.series.Series
"""
ma5 = gs['Adj Close'].rolling(window=5).mean()

print(ma5.tail())

"""
정확한 이평선을 위해 거래량이 0인 날은 제외
"""
for j, i in enumerate(gs['Volume']):
    if i == 0:
        print(j)
        print(gs.iloc[[j], :])

new_gs = gs[gs['Volume'] != 0]

for j, i in enumerate(new_gs['Volume']):
    if i == 0:
        print(i != 0)
        print(new_gs.iloc[[j], :])

new_gs1 = gs[gs['Volume'] > 0]

for j, i in enumerate(new_gs1['Volume']):
    if i == 0:
        print(i != 0)
        print(new_gs1.iloc[[j], :])

ma5 = new_gs['Adj Close'].rolling(window=5).mean()

print(ma5.tail())
"""
DataFrame에 칼럼을 추가하려면 insert 메서드를 사용.
"""
new_gs.insert(len(new_gs.columns), "MA5", ma5)

print(new_gs)
"""
20, 60, 120 이평선 추가
"""
ma20 = new_gs['Adj Close'].rolling(window=20).mean()
ma60 = new_gs['Adj Close'].rolling(window=60).mean()
ma120 = new_gs['Adj Close'].rolling(window=120).mean()

new_gs.insert(len(new_gs.columns), "MA20", ma20)
new_gs.insert(len(new_gs.columns), "MA60", ma60)
new_gs.insert(len(new_gs.columns), "MA120", ma120)

print(new_gs)

import matplotlib.pyplot as plt

plt.plot(new_gs.index, new_gs['Adj Close'], label='Adj Close')
plt.plot(new_gs.index, new_gs['MA5'], label='MA5')
plt.plot(new_gs.index, new_gs['MA20'], label='MA20')
plt.plot(new_gs.index, new_gs['MA60'], label='MA60')
plt.plot(new_gs.index, new_gs['MA120'], label='MA120')

"""
legend 함수 = 범례를 표시하기 위해 사용, loc 인자를 통해 범례 표시 위치 지정. best는 자동
grid 함수 = 격자줄 표시
"""
plt.legend(loc='best')
plt.grid()
plt.show()
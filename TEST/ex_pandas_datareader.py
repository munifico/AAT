import pandas_datareader.data as web
import datetime

start = datetime.datetime(2020, 3, 2)

end = datetime.datetime(2020, 3, 10)
"""
DataReader 함수
첫 번째 인자로 조회할 종목에 대한 정보
두 번째 인자로 데이터를 가져올 소스에 대한 정보
세 번째 인자로 조회 기간의 시작일
네 번째 인자로 조회 기간의 종료일

DataReader 함수는 DataFrame 객체를 반환
야후 파이낸스는 수정 종가도 제공
수정 종가는 분할, 배당, 배분, 신주 발생이 된 경우를 고려해 주식 가격을 조정해둔 가격.
"""
gs = web.DataReader("078930.KS", "yahoo", start, end)

print(gs)
"""
DataFrame 객체를 요약해서 볼 수 있다.
.info()
"""
print(gs.info())
"""
DataReader 함수를 호출할 때 명시적으로 조회 기간을 입력하지 않으면 5년전부터 오늘까지의 데이터를 얻어온다.
"""
gs = web.DataReader("078930.KS", "yahoo")

print(gs.info())

"""
파이썬에서 그래프를 그릴 때는 matplotlib라는 패키지를 주로 사용.
그래프는 matplotlib 패키지의 pyplot라는 모듈을 사용

pyplot 모듈에는 그래프를 그리는 plot 함수가 있다.
인자값 = 그래프로 표현하려는 데이터
"""
import matplotlib.pyplot as plt

plt.plot(gs['Adj Close'])
plt.show()
print(gs.index)
plt.plot(gs.index, gs['Adj Close'])
plt.show()
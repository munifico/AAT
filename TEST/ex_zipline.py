"""
Zipline 알고리즘 트레이딩 라이브러리
Zipline을 이용한 백테스팅(backtesting) 환경 꾸미기
백 테스팅은 개발한 알고리즘을 과거 데이터를 사용해 검증해보는 것

오픈소스이며 pandas, Matplotlib, Scipy 같은 파이썬 라이브러리와 쉽게 연동
https://www.zipline.io/ 에서 파이썬 버전 체크 필요 / 현재 3.5
zipline을 pip install할때 파이썬 버전에 맞는 VC++ 컴파일러가 필요하다.
3.5 이상은 VC++ 14 컴파일러.
Visual C++ 2019에 설치되어 있음

호환성 에러 보류

"""
from zipline.api import order, symbol
import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2016, 1, 2)

data = web.DataReader("AAPL", "yahoo", start, end)

# plt.plot(data.index, data['Adj Close'])
# plt.show()
"""
Zipline을 이용해 알고리즘을 백테스팅 하기 위해서는 initialize와 handle_data라는 함수를 구현해야한다.
Zipline 백테스팅 시뮬레이터는 시뮬레이션을 수행하기 전에 항상 initialize 함수를 호출한다.
시뮬레이션에 사용할 초기 투자 금액, 거래 수수료를 initialize 함수에서 설정.

실제 거래 알고리즘은 handle_data라는 함수에서 구현.
Zipline 시뮬레이터는 시뮬레이션을 수행하는 동안 거래일마다 handle_data를 호출.

"""

def initialize(context):
    pass
"""
Zipline 백테스팅 시뮬레이션.
order = 주문을 실행하는 함수.
symbol = 참조할 데이터에 대한 심볼을 등록하는 함수

지금 함수는 order함수를 사용해 심볼이 'AAPL'인 주식 한 주를 매수하는 코드.
"""
def handle_data(context, data):
    order(symbol('AAPL'),1)

print(data.head())
"""
백테스팅에는 수정 종가만 사용.
기존의 DataFrame에서 'Adj Close' 칼럼만 선택해 새로운 DataFrame 객체를 생성.
"""
data = data[['Adj Close']]

print(data.head())
"""
handle_data 함수를 구현할 때 symbol("AAPL")을 사용했는데 이것은 DataFrame 객체에서 선택할 칼럼 인덱스를 의미.
DataFrame 객체의 칼럼 인덱스 값을 'Adj Close'에서 'AAPL'로 변경.
"""
data.columns = ["AAPL"]

print(data.head())
"""
DataFrame 객체의 인덱스 값을 협정 세계시(UTC)로 변경.
"""
data = data.tz_localize("UTC")

print(data.head())

from zipline.algorithm import TradingAlgorithm

algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data)

result = algo.run(data)

print(result)
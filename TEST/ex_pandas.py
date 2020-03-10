"""
빅 데이터
Volume, Velocity, Variety
양, 데이터의 입출력 속도, 다양성의 세가지 V를 가진 데이터를 뜻함.

Pandas의 Series는 1차원 데이터를 다루는데 효과적인 자료구조
DataFrame은 행과 열로 구성된 2차원 데이터를 다루는 데 효과적인 자료구조
"""

"""
리스트 반복문을 통해 쉽게 데이터를 관리 할 수 있다.
다양한 메서드 (insert, append, index) 등이 제공
"""
mystock = ['kakao', 'naver']

print(mystock[0])
print(mystock[1])

"""
튜플은 리스트와 달리 수정할 수 없지만 리스트보다 속도가 빠르다.
"""
mystock = ('kakao', 'naver')

print(mystock[0])
print(mystock[1])

"""
딕셔너리는 키-값(key-value)라는 쌍으로 데이터를 저장.
키를 가지고 빠르게 값을 찾을 수 있는 자료구조
A=B이다 라는 구조에서 편하게 쓰일 듯
"""
exam_dic = {'key1': 'room1', 'key2': 'room2'}

print(exam_dic['key1'])
print(exam_dic['key2'])

"""
pandas의 Series는 파이썬의 리스트, 딕셔너리와 비슷하다.
Series는 클래스
생성자로 파이썬 리스트를 넘겨주면 해당 값을 포함하는 Series 객체를 생성

Series 객체는 값, 값과 연결된 인덱스 값을 동시에 저장
"""
from pandas import Series, DataFrame

kakao = Series([92600, 92400, 92100, 94300, 92300])
print(kakao)
"""
Series 객체 내의 데이터는 1차원으로 저장돼 있지만 파이썬의 딕셔너리와 유사하게 값과 대응되는 인덱스 값이 서로 연결돼 있다.
"""
kakao2 = Series([92600, 92400, 92100, 94300, 92300], index=['2016-02-19',
                                                            '2016-02-18',
                                                            '2016-02-17',
                                                            '2016-02-16',
                                                            '2016-02-15'])
print(kakao2)

for date in kakao2.index:
    print(date)

for ending_prince in kakao2.values:
    print(ending_prince)

mine = Series([10, 20, 30], index=['naver', 'sk', 'kt'])
friend = Series([10, 30, 20], index=['tk', 'naver', 'sk'])
"""
인덱스의 순서가 서로 다른 경우에도 알아서 인덱싱이 같은 값끼리 덧셈 연산을 수행한다.
"""
merge = mine + friend
print(merge)

"""
pandas의 DataFrame 자료구조.
DataFrame은 여러 개의 칼럼(Column)으로 구성된 2차원 형태의 자료구조.
DataFrame 객체를 생성하는 가장 쉬운 방법은 파이썬의 딕셔너리를 사용하는 것.

Series와 유사하게 정수값으로 자동 인덱싱된 것을 확인 할 수 있다.

DataFrame에 있는 각 칼럼은 Series 객체이다.
DataFrame는 인덱스가 같은 여러개의 Series 객체로 구성된 자료구조.
"""
raw_data = {'col0':[1, 2, 3, 4],
            'col1':[10, 20, 30, 40],
            'col2':[100, 200, 300, 400]}

data = DataFrame(raw_data)
print(data)

"""
시가, 고가, 저가, 종가
open, high, low, close
OHLC
"""
daeshin = {'open':  [11650, 11100, 11200, 11100, 11000],
           'high':  [12100, 11800, 11200, 11100, 11150],
           'low' :  [11600, 11050, 10900, 10950, 10900],
           'close': [11900, 11600, 11000, 11100, 11050]}

daeshin_day = DataFrame(daeshin)
print(daeshin_day)

"""
cloumns 인자는 컬럼의 순서를 지정
"""
daeshin_day = DataFrame(daeshin, columns=['open', 'high', 'low', 'close'])

"""
DataFrame 객체를 생성하는 시점에 index를 지정할 수 있다.
"""
date = ['16.02.29', '16.02.26', '16.02.25', '16.02.24', '16.02.23']
daeshin_day = DataFrame(daeshin, columns=['open', 'high', 'low', 'close'], index=date)

"""
DataFrame 객체는 칼럼으로 접근 할 수 있다.
"""
print(daeshin_day['close'])

"""
DataFrame 객체는 loc 메서드를 사용해서 인덱스 값을 가진 로우 데이터를 가져올 수 있다.
"""
print(daeshin_day.loc['16.02.24'])

"""
DataFrame 객체의 칼럼에 접근하려면 칼럼 이름을 지정.
로우에 접근하려면 loc 메서드를 통해 인덱스 값을 지정.
"""

print(daeshin_day.columns)
print(daeshin_day.index)

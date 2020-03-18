"""
pandas의 DataFrame은 2차원 자료구조

pandas의 DataFrame 객체를 데이터 베이스에 저장하는 방법 & 저장된 데이터를 DataFrame 객체로 로드하는 방법
"""

# import pandas as pd
# from pandas import Series, DataFrame
# import sqlite3
#
# raw_data = {'col0': [1, 2, 3, 4], 'col1': [10, 20, 30, 40], 'col2': [100, 200, 300, 400]}
# df = DataFrame(raw_data)
#
# con = sqlite3.connect("D:\source\AAT\TEST\\kospi.db")

"""
pandas의 DataFrame 클래스는 DataFrame 객체 내의 데이터를 데이터 베이스로 저장하기 위해
to_sql 메서드 제공
명시적으로 SQL 구문을 사용하지 않고도 to_sql 메서드로 데이터 저장 가능.
인자값 1. 테이블, 2. Connection 객체
테이블에 df 객체의 내용을 저장.

DataFrame.to_sql(name, con, flavor='sqlite', schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)

파라미터	설명
name	SQL 테이블 이름으로 파이썬 문자열로 형태로 나타낸다.
con	Cursor 객체
flavor	사용한 DBMS를 지정할 수 있는데 'sqlite' 또는 'mysql'을 사용할 수 있다. 기본값은 'sqlite'이다.
schema	Schema를 지정할 수 있는데 기본값은 None이다.
if_exists	데이터베이스에 테이블이 존재할 때 수행 동작을 지정한다. 'fail', 'replace', 'append' 중 하나를 사용할 수 있는데 기본값은 'fail'이다. 'fail'은 데이터베이스에 테이블이 있다면 아무 동작도 수행하지 않는다. 'replace'는 테이블이 존재하면 기존 테이블을 삭제하고 새로 테이블을 생성한 후 데이터를 삽입한다. 'append'는 테이블이 존재하면 데이터만을 추가한다.
index	DataFrame의 index를 데이터베이스에 칼럼으로 추가할지에 대한 여부를 지정한다. 기본값은 True이다.
index_label	인덱스 칼럼에 대한 라벨을 지정할 수 있다. 기본값은 None이다.
chunksize	한 번에 써지는 로우의 크기를 정숫값으로 지정할 수 있다. 기본값은 None으로 DataFrame 내의 모든 로우가 한 번에 써진다.
dtype	칼럼에 대한 SQL 타입을 파이썬 딕셔너리로 넘겨줄 수 있다.

"""
# df.to_sql('test', con)

"""
DataFrame 객체에 많은 로우가 있어, 이를 데이터베이스 한 번에 쓰는 경우 패킷 크기 제약으로 에러가 발생할 수 있다.
한 번에 데이터 베이스로 저장될 로우의 개수를 지정할 수 있다.
"""
# df.to_sql('test', con, chunksize=1000)

import pandas as pd
from pandas import Series, DataFrame
import sqlite3

con = sqlite3.connect("D:\source\AAT\TEST\\kospi.db")

"""
read_sql 함수
인자값 1. SQL 구문, 2. Connection 객체, index_col 인자는 DataFrame 객체에서 인덱스로 사용될 칼럼; 기본값은 None -> 0부터 시작하는 정숫값이 인덱스로 할당

"""
df = pd.read_sql("SELECT * FROM kakao", con, index_col=None)

print(type(df))

"""
이미 DataFrame의 인덱스에 해당하는 칼럼이 존재하는 경우.
해당하는 칼럼의 이름을 index_col 인자로 전달.
"""
df = pd.read_sql("SELECT * FROM test", con, index_col='index')

print(df)
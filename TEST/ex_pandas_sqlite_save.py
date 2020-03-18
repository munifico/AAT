"""
Pandas를 이용한 주가 데이터 저장
"""

import pandas as pd
import pandas_datareader.data as web
import datetime
import sqlite3

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2016, 1, 2)

df = web.DataReader("078930.KS", "yahoo", start, end)

print(df.head)

con = sqlite3.connect("D:\source\AAT\TEST\\kospi.db")

"""
DataReader 함수는 DataFrame 객체를 만듬
DataFrame 객체에서 to_sql 메서드를 사용.
"""
df.to_sql('078930', con, if_exists='replace')

readed_df = pd.read_sql("SELECT * FROM '078930'",con, index_col='Date')

print(readed_df)
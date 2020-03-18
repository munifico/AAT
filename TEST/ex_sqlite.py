"""
DataFrame 형태로 데이터를 제공하는 야후 Finance나 구글 Finance가 편리.
국내의 모든 종목에 대한 데이터를 제공 x, 틱 단위의 데이터 x
국내 증권사 API는 DataFrame 형태는 아니지만
모든 종목에 대한 데이터를 내려받을 수 있음.
일봉도 꽤 오랜 기간 동안의 데이터를 내려 받을 수 있음.
틱 데이터는 데이터의 양이 많아서 최근 거래일로부터 일정 기간 동안의 데이터만 제공

즉.
틱 데이터의 경우 증권사 API를 이용해 데이터를 PC에 주기적으로 받아 두어야함.
"""

"""
sqlite3 - 파이썬 표준 라이브러리
데이터 베이스를 쉽게 이용할 수 있다.

.version  sqlite3 모듈 버전
.sqlite_version  SQLite 버전
"""

import sqlite3

print(sqlite3.version)
print(sqlite3.sqlite_version)

"""
데이터 베이스 생성은 sqlite3 모듈의 
connect 함수 사용.
인자값 1. 생성할 데이터베이스 파일의 경로 및 이름.
 -> Connection 객체로 데이터 베이스를 조작.
"""
con = sqlite3.connect("D:\source\AAT\TEST\\kospi.db")
print(type(con))
sqlite3.Connection


"""
DBMS에서는 SQL 구문을 호출해서 데이터를 조작.
SQL 구문을 호출하려면 Cursor 객체가 필요.
Connection 객체인 con을 사용해 Cursor 객체 생성.
"""
# cursor = con.cursor()

"""
열 (칼럼 (column)), 행 (로우(row)), 테이블 (칼럼 & 로우의 2차원 데이터 구조)
SQL 구문을 사용.
CREATE TABLE (table)(~)= 테이블을 만든다.
파이썬에서 SQL 구문을 실행하려면 Cursor 객체의 execute 메서드 사용.
인자값 1. SQL 구문

INSERT INTO (table) VALUES(~) = 테이블 안으로 VALUES를 삽입한다.

.commit() 메서드 - 지금까지 작업한 내용을 DB에 반영.
.close() 메서드 - DB 연결을 닫는다.
"""
# cursor.execute("CREATE TABLE kakao(Date text, Open int, High int, Low int, Closing int, Volumn int)")
# cursor.execute("INSERT INTO kakao VALUES('16.06.03', 97000, 98600, 96900, 98000, 321405)")
# con.commit()
# con.close()


import sqlite3

con = sqlite3.connect("D:\source\AAT\TEST\\kospi.db")
cursor = con.cursor()

"""
SELECT * FROM (table) - 테이블의 모든 것을 선택하라.

fetchone 메서드 - 선택한 테이블로부터 로우 단위로 데이터를 읽음 / 호출한 로우는 사라짐 / 리스트에 저장해서 인덱싱으로 사용
fetchall 메서드 - 한 번에 모든 로우를 읽기 위해 사용.
"""
cursor.execute("SELECT * FROM kakao")
print(cursor.fetchone())
print(cursor.fetchone())

cursor.execute("SELECT * FROM kakao")
print(cursor.fetchall())

cursor.execute("SELECT * FROM kakao")
kakao = cursor.fetchall()
print(kakao[0][0])

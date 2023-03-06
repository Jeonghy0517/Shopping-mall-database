#csv 파일
#쉼표(,)로 구분한 텍스트 데이터 및 텍스트 파일
#csv 파일을 데이터 베이스 프로그램에 바로 import 해서 테이블로 사용이 가능 => 대부분의 업무에서 사용되는 데이터 형식

import csv

#csv 파일 읽기
result = []
with open('product_list.csv', 'r', encoding='euc-kr') as f:
    reader = csv.reader(f)
    for line in reader:
        result.append(line)
        print(line)

#csv 파일 수정
#방법1
with open('product_list.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(result) #이전 레코드
    writer.writerow(['9','양말','5000']) #신규 레코드

#방법2
result.append(['9','양말','5000'])

with open('product_list.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(result)

#----------------------------------------------------------------------------------------------------------------------
#데이터베이스 연결
#sqlite3 : SQLite 데이터베이스를 사용하는데 필요한 인터페이스 파이썬 표준 라이브러리
import sqlite3
print(sqlite3.version)
print(sqlite3.sqlite_version)

conn = sqlite3.connect('test.db')
c = conn.cursor() #커서 생성

# query = '''CREATE TABLE test2 (ID INTEGER PRIMARY KEY, PRODUCT_NAME TEXT, PRICE INTEGER)'''
# c.execute(query)

conn.close()

#----------------------------------------------------------------------------------------------------------------------
#데이터 불러오기, 조회하기
#sqlite3 에서 데이터 조회 방법에는 fetchone(), fetchmany(), fetchall() 3 가지 방법을 사용
#SELECT 문을 사용한 조회 결과 범위에서 실제 가져오는 row 수를 결정

#DB 연결
import sqlite3
import pandas as pd

conn = sqlite3.connect("chadwick.db")
c = conn.cursor()

c.execute('''SELECT * FROM sqlite_master WHERE type="table"''')
print(pd.DataFrame(c.fetchall())) #레코드를 배열형식으로 저장

#데이터 조회
c.execute('''SELECT * FROM Parks''') #전체 데이터 조회
print(pd.DataFrame(c.fetchall())) #전체 로우 선택

print(pd.DataFrame(c.fetchone())) #1개 로우 선택
print(pd.DataFrame(c.fetchmany(size=3))) #지정 로우 선택

#특정 데이터 조회
cur = c.execute('''SELECT * FROM Parks''')
print(cur.description) #컬럼 키 확인

#특정 row만 가져오기
c.execute('''SELECT * FROM Parks WHERE state = ?''', ('NY',))
print(pd.DataFrame(c.fetchall()))

conn.close()

#----------------------------------------------------------------------------------------------------------------------
#데이터 삽입, 수정, 삭제
#데이터 삽입 (INSERT)
import sqlite3
conn = sqlite3.connect("test.db")
c = conn.cursor()

query = '''CREATE TABLE test (ID INTERGER PRIMARY KEY, PRODUCT_NAME TEXT, PRICE INTERGER)'''
c.execute(query) #테이블 생성

#테이블 생성 확인
c.execute('''SELECT * FROM sqlite_master WHERE type="table"''')
print(c.fetchall())

#INSERT 방법 1. 열(키) 항목 순서를 정확히 알고 있는 경우
# c.execute("INSERT INTO test VALUES(10,'모자',150000)")
# conn.commit()

# c.execute("INSERT INTO test VALUES(11,'코트',200000)")
# conn.commit()

#INSERT 방법 2. 열(키) 항목 순서를 정확히 모르는 경우
#데이터 삽입
# c.execute("INSERT INTO test(PRODUCT_NAME, PRICE, ID) VALUES(?,?,?)", ('티셔츠', 20000, 13))
# conn.commit()

#INSERT 방법 3. 여러 데이터를 한번에 삽입하고 싶은 경우
#테이블 내용 삭제
c.execute("DELETE FROM test")
conn.commit()

#추가 할 상품 리스트
product_list = [[1, '모자', 15000],
                [2, '코트', 200000],
                [3, '티셔츠', 20000],
                [4, '블라우스', 55000],
                [5, '가디건', 45000],
                [6, '청바지', 50000],
                [7, '구두', 150000],
                [8, '가방', 170000]]

#데이터 여러 줄 삽입
c.executemany("INSERT INTO test(ID, PRODUCT_NAME, PRICE) VALUES(?,?,?)", product_list)
conn.commit()

#데이터 수정 (UPDATE)
#UPDATE 방법 1. 튜플 형태로 수정
c. execute("UPDATE test SET PRODUCT_NAME = ? WHERE ID = ?", ('슬랙스', 6))
conn.commit()

#UPDATE 방법 2. 딕셔너리 형태로 수정
c. execute("UPDATE test SET PRODUCT_NAME = :price WHERE ID = :id", {"price":55000, "id":6})
conn.commit()

#UPDATE 방법 3. %s 표시자 사용
c. execute("UPDATE test SET PRODUCT_NAME = '%s' WHERE ID = '%s'" % ('트랜치코트', 2))
conn.commit()

#데이터 삭제 (DELECT)
#DELETE 방법 1.튜플 형태로 삭제
c.execute("DELETE FROM test WHERE ID =?", (8,))
conn.commit()

#DELETE 방법 2. 딕셔너리 형태로 삭제
c.execute("DELETE FROM test WHERE PRODUCT_NAME = :product_name", {'product_name':'슬랙스'})
conn.commit()

c.execute('''SELECT * FROM test''')
print(c.fetchall())

#DELETE 방법 3. 전체 삭제
c.execute("DELETE FROM test")
conn.commit()

conn.close()

#----------------------------------------------------------------------------------------------------------------------
#데이터 백업하기
#iterdump : 데이터 베이스를 백업할 때 사용하는 모듈
#.sql 파일 확장자로 테이블을 다시 복원할 수 있는 쿼리문을 저장

import sqlite3
conn = sqlite3.connect("test.db")
c = conn.cursor()

#추가 할 상품 리스트
product_list = [[1, '모자', 15000],
                [2, '코트', 200000],
                [3, '티셔츠', 20000],
                [4, '블라우스', 55000],
                [5, '가디건', 45000],
                [6, '청바지', 50000],
                [7, '구두', 150000],
                [8, '가방', 170000]]

#데이터 여러 줄 삽입
c.executemany("INSERT OR REPLACE INTO test (ID, PRODUCT_NAME, PRICE) VALUES(?,?,?)", product_list)
conn.commit()

#iterdump 내용 확인
for line in conn.iterdump():
    print(line)

#데이터 베이스 백업 파일 생성
with conn:
    with open('backup.sql', 'w') as f:
        for line in conn.iterdump():
            f.write('%s\n' % line)
        print('Completed.')

c.execute("DROP TABLE test") #테이블 삭제
conn.commit()

#백업 SQL 파일 로딩
with open('backup.sql', 'r') as sql_file:
    sql_script = sql_file.read()

print(sql_script)

c.execute("DROP TABLE test2") #테이블 삭제
conn.commit()

#SQL 스크립트 실행
c.executescript(sql_script)
conn.commit()
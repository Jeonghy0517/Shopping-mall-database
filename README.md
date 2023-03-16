# Shopping-mall-database
## 쇼핑몰 데이터 베이스를 연결해 주문정보 저장하고 확인하는 프로그램
---
### 사용한 Python 라이브러리

+ **sqlite3**

  * SQLite 데이버페이스를 사용하는데 필요한 인터페이스, 파이썬 표준 라이브러리
  
  * SQLite3에서 데이터를 조회하는 방법엔 fetchone(), fetchmany(), fetchall() 3가지 방법이 있음
  
  * SELECT문을 사용한 조회 결과 범위에서 실제 가져오는 ROW 수를 결정

+ **iterdump**

  * 데이터 베이스를 백업할 때 사용하는 모듈
  
  * .sql 파일 확장자로 테이블을 다시 복원할 수 있는 쿼리문을 저장
  

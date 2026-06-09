# Library Rental System

PostgreSQL과 FastAPI를 활용한 도서 대여 관리 시스템

## 프로젝트 소개

본 프로젝트는 데이터베이스 과목 프로젝트로 개발한 웹 기반 도서 대여 시스템이다.

사용자 등록, 도서 등록, 도서 대여 및 반납 기능을 제공하며, PostgreSQL 데이터베이스와 FastAPI를 연동하여 구현하였다.

주요 목표는 다음과 같다.

* PostgreSQL을 이용한 관계형 데이터베이스 설계
* FastAPI와 DBMS 연동
* JOIN Query 활용
* Transaction 처리
* 동시성 제어(FOR UPDATE)
* Index를 활용한 성능 최적화
* Jinja2 기반 웹 인터페이스 구현

---

# 기술 스택

* Backend : FastAPI
* Database : PostgreSQL
* ORM : SQLAlchemy
* Template Engine : Jinja2
* Server : Uvicorn
* Container : Docker

---

# ERD

```mermaid
erDiagram
    USERS ||--o{ RENTALS : rents
    BOOKS ||--o{ RENTALS : rented

    USERS {
        INT id
        STRING name
        STRING email
        DATETIME created_at
    }

    BOOKS {
        INT id
        STRING title
        STRING author
        INT stock
        DATETIME created_at
    }

    RENTALS {
        INT id
        INT user_id
        INT book_id
        DATETIME rental_date
        DATETIME return_date
        STRING status
    }
```

## Text ERD

```text
USERS
-----
id PK
name
email
created_at

USERS 1 : N RENTALS

RENTALS
-------
id PK
user_id FK
book_id FK
rental_date
return_date
status

BOOKS 1 : N RENTALS

BOOKS
-----
id PK
title
author
stock
created_at
```

---

# 시스템 구조

```mermaid
flowchart LR
    A["Web Browser"]
    B["Jinja2 Template"]
    C["FastAPI"]
    D["SQLAlchemy"]
    E["PostgreSQL"]

    A --> B
    B --> C
    C --> D
    D --> E
```

```text
Web Browser
    ↓
Jinja2 Template
    ↓
FastAPI
    ↓
SQLAlchemy
    ↓
PostgreSQL
```

---

# 데이터베이스 핵심 구현 내용

## 1. Relation 설계

본 프로젝트는 USERS, BOOKS, RENTALS의 세 개 릴레이션으로 구성된다.

### USERS

사용자 정보를 저장하는 릴레이션

| 속성         | 설명      |
| ---------- | ------- |
| id         | 기본키(PK) |
| name       | 사용자 이름  |
| email      | 이메일     |
| created_at | 생성일     |

### BOOKS

도서 정보를 저장하는 릴레이션

| 속성         | 설명      |
| ---------- | ------- |
| id         | 기본키(PK) |
| title      | 도서명     |
| author     | 저자      |
| stock      | 재고      |
| created_at | 생성일     |

### RENTALS

도서 대여 기록을 저장하는 릴레이션

| 속성          | 설명           |
| ----------- | ------------ |
| id          | 기본키(PK)      |
| user_id     | USERS 참조(FK) |
| book_id     | BOOKS 참조(FK) |
| rental_date | 대여일          |
| return_date | 반납일          |
| status      | 대여 상태        |

### 릴레이션 관계

* USERS 1 : N RENTALS
* BOOKS 1 : N RENTALS

즉, 한 명의 사용자는 여러 권의 도서를 대여할 수 있으며, 하나의 도서는 여러 번 대여 기록을 가질 수 있다.

---

## 2. Query 구현

본 프로젝트에서는 INSERT, UPDATE, SELECT, JOIN Query를 사용하였다.

### 사용자 등록

```sql
INSERT INTO users(name, email)
VALUES ('Kim', 'kim@test.com');
```

### 도서 등록

```sql
INSERT INTO books(title, author, stock)
VALUES ('Database', 'Hong', 3);
```

### 도서 반납

```sql
UPDATE rentals
SET status='RETURNED'
WHERE id=1;
```

### JOIN Query

대여 현황 조회 시 rentals 테이블만으로는 사용자 이름과 도서 제목을 확인할 수 없으므로 JOIN Query를 사용하였다.

```sql
SELECT
    r.id AS rental_id,
    u.name AS user_name,
    b.title AS book_title,
    r.rental_date,
    r.return_date,
    r.status
FROM rentals r
JOIN users u
    ON r.user_id = u.id
JOIN books b
    ON r.book_id = b.id;
```

이를 통해 사용자 정보, 도서 정보, 대여 정보를 하나의 결과로 조회할 수 있다.

---

## 3. Transaction 처리

도서 대여 기능은 여러 개의 데이터베이스 작업이 하나의 논리적 작업으로 수행된다.

대여 시 수행되는 작업은 다음과 같다.

1. 도서 재고 확인
2. 재고 감소
3. 대여 기록 생성
4. Commit

예를 들어 재고는 감소했지만 대여 기록이 생성되지 않는 경우 데이터 불일치가 발생한다.

이를 방지하기 위해 하나의 Transaction으로 처리하였다.

```sql
BEGIN;

UPDATE books
SET stock = stock - 1
WHERE id = ?;

INSERT INTO rentals(
    user_id,
    book_id,
    rental_date,
    status
)
VALUES(
    ?,
    ?,
    CURRENT_TIMESTAMP,
    'RENTED'
);

COMMIT;
```

오류 발생 시에는 ROLLBACK을 수행하여 이전 상태로 복구한다.

---

# 동시성 제어

동일 도서에 대한 동시 대여 요청을 처리하기 위해 FOR UPDATE를 사용하였다.

```sql
SELECT *
FROM books
WHERE id = ?
FOR UPDATE;
```

이를 통해 동시에 여러 사용자가 동일한 도서를 대여할 때 발생할 수 있는 Lost Update 문제를 방지하였다.

---

# 성능 최적화

도서 제목 검색 성능 향상을 위해 Index를 생성하였다.

```sql
CREATE INDEX idx_books_title
ON books(title);
```

## 성능 측정 결과

| 구분       | 실행 계획      | 실행 시간    |
| -------- | ---------- | -------- |
| 인덱스 적용 전 | Seq Scan   | 0.397 ms |
| 인덱스 적용 후 | Index Scan | 0.029 ms |

약 13.7배의 검색 성능 향상을 확인하였다.

실험 데이터는 약 10,000건의 도서 데이터를 사용하였다.

---

# 주요 기능

## 사용자 관리

* 사용자 등록
* 사용자 조회

## 도서 관리

* 도서 등록
* 도서 조회

## 도서 대여

* 도서 대여
* 도서 반납
* 재고 자동 감소 및 증가

## 대여 현황 조회

* JOIN Query 기반 대여 현황 조회
* 대여 상태(RENTED / RETURNED) 확인

## 관리자 페이지

* 사용자 등록
* 도서 등록
* 등록된 사용자 조회
* 등록된 도서 조회

---

# 실행 방법

## PostgreSQL 실행

```powershell
docker start library-postgres
```

## 가상환경 활성화

```powershell
.\venv\Scripts\Activate.ps1
```

## 서버 실행

```powershell
uvicorn app.main:app --reload
```

## 샘플 데이터 입력

```powershell
Get-Content .\sql\sample_data.sql | docker exec -i library-postgres psql -U postgres -d librarydb
```

---

# 구현 결과

## 구현 항목

* PostgreSQL 데이터베이스 구축
* FastAPI REST API 구현
* SQLAlchemy ORM 연동
* Relation 설계 구현
* JOIN Query 구현
* Transaction 처리 구현
* FOR UPDATE 기반 동시성 제어 구현
* Index 기반 성능 최적화 구현
* Jinja2 기반 웹 페이지 구현
* 관리자 페이지 구현

---

# 접속 주소

## 웹 메인 페이지

http://localhost:8000

## 관리자 페이지

http://localhost:8000/admin

## 대여 현황 페이지

http://localhost:8000/rentals-page

## Swagger

http://localhost:8000/docs

## .env 파일
DATABASE_URL=postgresql://postgres:1234@localhost:5432/librarydb 

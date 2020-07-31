# File CRUD RESTful API with FLask



### Required Settings

- Python 3.6.10 (for `fast.ai`, but this package is not used here)
- flask, flask-restful



### Requirements

- 파일로  CRUD 작업을 수행하는  RESTful API를 구현한다.
-  파일은 데이터베이스에 저장하지 않고 메모리 내의 딕셔너리를 데이터 소스로 사용한다.
- 파일은 다음 속성 또는 필드를 갖는다.
  -  id: 정수 식별자
  -  file: 파일
  -  creation_date: 생성 날짜 및 시간
  -  label: 파일의 종류
- 이 API에서 지원해야하는 HTTP 동사 / 범위 / 의미
  - `GET` / 파일 컬렉션 / 컬렉션 내에 저장된 모든 파일을 얻음
  - `GET` / 파일 / 단일 파일을 받아 옴
  - `POST` / 파일 컬렉션 / 컬렉션 내의 새 파일 생성
  - `PATCH` / 파일 / 기존 파일의 label 필드를 업데이트
  - `DELETE` / 파일 / 기존 파일을 삭제


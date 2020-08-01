# File Upload RESTful API with Flask

업로드된 이미지 파일을 딥러닝 기반 분류기로 통과시키고 이미지의 class를 저장하기 위한 기본 틀이다.

여기서는 단순히 업로드된 이미지의 사이즈를 읽고 이를 메모리의 딕셔너리 소스 내에 저장한다.



### Required Settings

- Python 3.6.10 (for `fast.ai`, but this package is not used here)
- flask, flask-restful



### Requirements

- 이미지 파일을 업로드하여 이미지의 사이즈를 저장하고 이 사이즈를 읽을 수 있는  RESTful API를 구현한다.
- 이미지 파일이 업로드 되면 다음 속성 또는 필드를 갖는 정보가 저장된다.
  -  id: 정수 식별자
  -  size: 이미지의 크기
  -  creation_date: 생성 날짜 및 시간
- 이 API에서 지원해야하는 HTTP 동사 / 범위 / 의미
  - `GET` / 파일 정보 / 단일 파일 정보를 받아 옴
  - `POST` / 파일 정보 컬렉션 / 컬렉션 내의 새 파일 정보 생성
  - `DELETE` / 파일 / 기존 파일 정보를 삭제



### 각 HTTP 매서드가 수행하는 작업

- 메시지 컬렉션의 URL이 http://localhost:5000/api/files/ 일 때, 지정된 정수와 같은 id의 특정 메시지를 식별한다.

- `POST http://localhost:5000/api/files/`
  - 이미지를 업로드하고 서버는 이미지의 크기를 메모리 내의 딕셔너리에 저장
  - 서버는 최근에 추가된 메시지와 함께 `201 Created` 상태 코드와 JSON으로 직렬화된 JSON 본문을 반환
- `GET http://localhost:5000/api/files/{id}`
  - id와 일치하는 이미지의 정보를 받음
  - 서버는 이미지 정보 객체를 JSON으로 직렬화하고 `200 OK` 상태코드와 JSON 본문을 반환
  - 존재하지 않는 경우 `404 Not Found` 상태를 반환
- `DELETE http://localhost:5000/api/files/{id}`
  - id와 일치하는 이미지 정보를 제거, 관련된 항목을 삭제하고 `204 No Content` 반환
  - 지정된 id와 일치하는 이미지 정보가 없으면 `404 Not Found`
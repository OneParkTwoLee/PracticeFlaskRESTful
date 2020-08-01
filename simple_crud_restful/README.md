# Simple CRUD RESTful API With Flask



### Required Settings

- Python 3.8.2
- flask, flask-restful



### Requirements

- IoT 장치에 연결된 디스플레이에 나타낼 문자열 메시지를 구성해야 한다고 가정한다.

- 문자열 메시지로 CRUD 작업을 수행하는 RESTful API를 구현한다.
- 문자열 메시지는 데이터베이스에 저장하지 않고 메모리 내의 딕셔너리를 데이터 소스로 사용한다.
- 메시지는 다음 속성 또는 필드를 갖는다.
  - id: 정수 식별자
  - meassage: 문자열 메시지
  - duration: 메시지의 지속 시간
  - creation_date: 생성 날짜 및 시간
  - message_category: "경고" 및 "정보"와 같은 메시지 카테고리 설명
  - printed_times: 메시지가 디스플레이에 표시된 시간을 나타내는 정수 카운터
  - printed_once: 메시지가 적어도 한 번 디스플레이에 표시되었는지 나타내는 bool 값
- 이 API에서 지원해야하는 HTTP 동사 / 범위 / 의미
  - `GET` / 메시지 컬렉션 / 컬렉션 내에 저장된 모든 메시지를 얻어 이름의 오름차순으로 정렬
  - `GET` / 메시지 / 단일 메시지를 받아 옴
  - `POST` / 메시지 컬렉션 / 컬렉션 내에 새 메시지를 생성
  - `PATCH` / 메시지 / 기존 메시지의 필드를 업데이트
  - `DELETE` / 메시지 / 기존 메시지를 삭제



### 각 HTTP 매서드가 수행하는 작업

- 메시지 컬렉션의 URL이 http://localhost:5000/api/messages/ 일 때, 지정된 정수와 같은 id의 특정 메시지를 식별한다.
  - 예,  http://localhost:5000/api/messages/6 : id가 6인 메시지

- `POST http://localhost:5000/api/messages/`
  - 새 메시지를 작성할 수 있음
  - 요청의 결과로 서버는 필드에 대해 제공된 값의 유효성을 검사하고 유효한 메시지인지 확인하고 딕셔너리에 이를 유지
  - 서버는 최근에 추가된 메시지와 함께 `201 Created` 상태 코드와 JSON으로 직렬화된 JSON 본문을 반환
- `GET http://localhost:5000/api/messages/{id}`
  - id와 일치하는 메시지를 받음
  - 메시지가 발견되면 서버는 메시지 객체를 JSON으로 직렬화하고 `200 OK` 상태코드와 JSON 본문을 반환
  - 존재하지 않는 경우 `404 Not Found` 상태를 반환
- `PATCH http://localhost:5000/api/messages/{id}`
  - id와 일치하는 메시지의 필드를 하나 이상 업데이트
  - 정상적인 경우 `200 OK` 상태 코드와 업데이트된 JSON 본문을 반환
  - 업데이트할 필드에 유효하지 않는 데이터를 제공하면 `400 Bad Request`, 지정된 id의 메시지를 찾지 못하면 `404 Not Found`

- `DELETE http://localhost:5000/api/messages/{id}`
  - id와 일치하는 메시지를 제거, 관련된 항목을 삭제하고 `204 No Content` 반환
  - 지정된 id와 일치하는 메시지가 없으면 `404 Not Found`
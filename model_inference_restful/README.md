# Model Inference RESTful API with Flask



### Required Settings

- Python 3.6.10
- flask, flask-restful
- fast.ai



### Requirements

- 모델은 사자와 호랑이 이미지를 CNN을 기반으로 구분한다.

- 클라이언트에서 이미지를 업로드했을 때 모델은 이미지의 라벨을 추론하여 저장하고 이를 읽을 수 있는 RESTful API를 구현한다.
- 이미지 파일이 업로드 되면 다음 속성 또는 필드를 갖는 정보가 저장된다.
  -  id : 정수 식별자
  - size: 이미지의 크기
  - reasoning_time: 추론 시간
  - predicted_label: 이미지의 예측된 라벨
- 이 API에서 지원해야하는 HTTP 동사 / 범위 / 의미 
  - `GET` / 이미지 정보 / 단일 이미지의 정보를 받아 옴
  - `POST` / 이미지 정보 컬렉션 / 컬렉션 내의 새 이미지 정보 생성
  - `DELETE` / 이미지 정보 / 기존 이미지 정보를 삭제



### 각 HTTP 매서드가 수행하는 작업

- `POST http://localhost:5000/api/files/`
  - 이미지를 업로드하고 서버는 이미지의 정보를 메모리 내의 딕셔너리에 저장
  - 서버는 최근에 추가된 메시지와 함께 `201 Created` 상태 코드와 JSON으로 직렬화된 JSON 본문을 반환
- `GET http://localhost:5000/api/files/{id}`
  - id와 일치하는 이미지의 정보를 받음
  - 서버는 이미지 정보 객체를 JSON으로 직렬화하고 `200 OK` 상태코드와 JSON 본문을 반환
  - 존재하지 않는 경우 `404 Not Found` 상태를 반환
- `DELETE http://localhost:5000/api/files/{id}`
  - id와 일치하는 이미지 정보를 제거, 관련된 항목을 삭제하고 `204 No Content` 반환
  - 지정된 id와 일치하는 이미지 정보가 없으면 `404 Not Found`
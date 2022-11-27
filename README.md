# To-Do

**To-Do**는 간단한 할 일 목록 애플리케이션입니다.

## API

API 서버는 Flask 프레임워크로 개발되었습니다.

데이터베이스와 통신할 때는 SQLAlchemy([flask-sqlalchemy](https://github.com/pallets-eco/flask-sqlalchemy))를 사용합니다. 테이블을 관리하기 위해 Alembic([flask-migrate](https://github.com/miguelgrinberg/Flask-Migrate))를 사용하고 있습니다. 인증 시도의 5분 타이머는 [redis](https://redis.io)를 활용하고 있습니다. 키 값은 모두 `chick0/to-do:`로 시작하고 용도와 대상을 가리키는 이메일 형태로 이루어져있습니다.

모든 설정 파일들은 환경변수에서 가져오고, `.env`를 사용해 관리하고 있습니다.

모든 토큰은 JWT를 사용하고 있습니다. 토큰은 용도별로 다른 시크릿 키를 가지고 있습니다.

또 [pydantic](https://github.com/pydantic/pydantic)을 이용해 요청과 응답 값의 타입을 체크하고 있습니다.

# 설치 및 설정

## 주의사항

1. 데이터베이스는 MySQL 또는 MariaDB를 사용하는 것을 권장합니다. SQLAlchemy를 사용하고 있지만 다른 데이터베이스에서 테스트를 진행하지 않았습니다.
2. 이 프로그램은 인증 시도 타이머 기능에 redis를 사용됩니다.
3. 이 프로그램은 인증 메일을 발송하기 위한 SMTP 서버가 필요합니다. 또 starttls를 사용해 세션을 암호화하고 있습니다.

## API

> 파이썬 3.9버전과 3.10버전에서 테스트되었습니다.

본 프로그램은 의존성 관리를 위해 [pip-tools](https://github.com/jazzband/pip-tools)를 사용하고 있습니다.

`pip-tools`를 사용한다면 다음의 방법을 통해 의존성을 설치 할 수 있습니다.

> 개발 환경이라면 `requirements-dev.in` 파일을 사용하는 것을 권장합니다.

1. 의존성 빌드 후 설치
    ```
    pip install pip-tools
    pip-compile
    pip-sync
    ```
2. 그냥 설치
    ```
    pip install pip-tools
    pip-sync
    ```

또는 기본 pip 명령어를 통해 설치 할 수 있습니다.

만약 파이썬 버전이 3.10보다 아래라면 `importlib-metadata` 패키지를 추가 설치해야합니다.

### 설정

모든 설정 정보는 환경 변수에서 가져오고, `.env` 파일을 이용해 관리하고 있습니다.
또는 다른 방법을 사용해 환경 변수를 관리할 수 있습니다.

`.env.example` 파일을 복사해 `.env`를 만든 다음 본인의 상황에 알맞게 수정하면 됩니다.

1. SQLALCHEMY_DATABASE_URI
    - 데이터베이스 접속 경로
    - `?charset=utf8mb4`를 추가하지 않으면 이모지 저장에 문제가 생깁니다.
2. REDIS_URL
    - redis 접속 경로
    - 이메일 인증과 비밀번호 재설정의 타이머를 위해 사용됩니다.
3. SMTP_HOST
    - SMTP 서버 주소
    - 이메일 전송을 위해 사용됩니다.
4. SMTP_PORT
    - SMTP 포트 번호
5. SMTP_USER
    - SMTP 사용자 아이디
6. SMTP_PASSWORD
    - SMTP 사용자 비밀번호
7. HOST
    - 프로토콜을 포함한 사이트 주소
    - 인증 이메일을 보낼때 사용됩니다.
8. HELP_EMAIL
    - 사용자가 도움을 받을 수 있는 (관리자가 확인 및 답변 할 수 있는) 이메일 주소
    - `:SMTP_USER`로 설정할 경우 SMTP 사용자 계정으로 설정합니다.
9. SCHEDULER_TIMEZONE
    - 스케쥴러의 시간대

### 데이터베이스

```
flask db upgrade
```

명령어를 통해 데이터베이스 모델을 업데이트 할 수 있습니다.

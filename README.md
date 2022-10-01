# To-Do

**To-Do**는 웹에서 사용하는 간단한 할 일 목록 웹 애플리케이션입니다.

> 해당 프로젝트는 API와 클라이언트가 동일한 저장소를 사용하고 있습니다.

## API

API 서버는 Flask 프레임워크로 개발되었습니다.

데이터베이스와 통신할 때는 SQLAlchemy([flask-sqlalchemy](https://github.com/pallets-eco/flask-sqlalchemy))를 사용합니다. 테이블을 관리하기 위해 Alembic([flask-migrate](https://github.com/miguelgrinberg/Flask-Migrate))를 사용하고 있습니다. 인증 시도의 5분 타이머는 [redis](https://redis.io)를 활용하고 있습니다. 키 값은 모두 `chick0/to-do:`로 시작하고 용도와 대상을 가리키는 이메일 형태로 이루어져있습니다.

모든 설정 파일들은 환경변수에서 가져오고, `.env`를 사용해 관리하고 있습니다.

모든 토큰은 JWT를 사용하고 있습니다. 토큰은 용도별로 다른 시크릿 키를 가지고 있습니다.

또 [pydantic](https://github.com/pydantic/pydantic)을 이용해 요청과 응답 값의 타입을 체크하고 있습니다.

추가로 '**선택적**' 의존성이 있습니다. 우선 [paste](https://github.com/cdent/paste) 패키지를 설치하면 웹 로그 기능이 활성화됩니다. 그리고 [flask-cors](https://github.com/corydolphin/flask-cors) 패키지를 설치하면 CORS 설정이 적용됩니다. CORS 기능이 선택적으로 제공되는 이유는 API 서버의 `/` 루트가 프론트엔드로 연결되어있기 때문입니다.

## 클라이언트

클라이언트는 Svelte 프레임워크로 개발되었습니다.

[svelte-spa-router](https://github.com/ItalyPaleAle/svelte-spa-router)를 이용해 해시 기반 라우팅을 사용하고 있습니다.

스타일은 자체 제작 스타일입니다. 폰트는 [Pretendard](https://github.com/orioncactus/pretendard)를 사용하고 있습니다. 해당 폰트는 공개중인 폰트와 다르게 영문, 기호, 일부 한글만 포함하고 있습니다. (총 2,927자) 또 브라우저간의 동일한 스타일을 위해 [minireset.css](https://github.com/jgthms/minireset.css)를 사용하고 있습니다.

웹 사이트의 아이콘의 경우에는 [Check Box Icon Tick Mark](https://pixabay.com/images/id-1294836/)를 수정해서 사용하고 있습니다.

모바일 환경의 개선을 위해 PWA를 사용하고 있습니다. 서비스 워커가 캐싱하는 종류는 프리캐시와 런타임 캐시로 분류됩니다. 프리캐시는 웹 사이트에 접속하면 캐싱하는 자주 변하지 않는 정적 컨텐츠 입니다. (아이콘, 폰트, 일부 스타일) 반대로 런타임 캐시는 코드가 수정되거나 빌드할 때마다 변경되는 파일입니다. 캐싱된 파일들은 [캐시 관리자](https://github.com/chick0/to-do/blob/master/public/cache.html)를 이용해 확인 및 삭제할 수 있습니다.

# 설치 및 설정

## 주의사항

1. 이 프로그램은 [MaxMind](https://www.maxmind.com)의 GeoLite2를 이용하고 있습니다.
    - `GeoLite2-Country.mmdb` 파일을 이 프로그램의 geoip 풀더에 추가해야합니다.
2. MySQL 또는 MariaDB를 사용하는 것을 권장합니다. SQLAlchemy를 사용하고 있지만 다른 데이터베이스에서 테스트를 진행하지 않았습니다.
3. 이 프로그램은 redis가 필요합니다. 인증 시도의 타이머에 사용됩니다.
4. 이 프로그램은 인증 메일을 발송하기 위한 SMTP 서버가 필요합니다. 또 starttls를 사용해 세션을 암호화하고 있습니다.

## 클라이언트

클라이언트의 경우에는 yarn을 이용해 의존성을 설치하고 빌드 할 수 있습니다.

다만 [릴리즈](https://github.com/chick0/to-do/releases) 메뉴에서 빌드된 결과물을 에셋에서 다운로드 할 수 있습니다.

## API

> 파이썬 3.9버전과 3.10버전에서 테스트되었습니다.

본 프로그램은 의존성 관리를 위해 [pip-tools](https://github.com/jazzband/pip-tools)를 사용하고 있습니다.

`pip-tools`를 사용한다면 다음의 방법을 통해 의존성을 설치 할 수 있습니다.

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

또 2가지 선택적 의존성이 있습니다.

1. Flask-CORS
    - 기본적으로 API 서버의 최상위 경로가 프론트와 연결되어 있지만, API 서버와 프론트를 분리해서 사용하는 경우에는 해당 의존성을 설치해야합니다.
2. Paste
    - 해당 패키지의 [TransLogger](https://github.com/cdent/paste/blob/master/paste/translogger.py)를 활용해 웹 로그 기능을 제공합니다.

### 서버 설정

서버의 모든 설정은 환경 변수에서 가져오고, `.env` 파일을 이용해 관리하고 있습니다.

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

# 저작권

@chick0이 작성한 API와 클라이언트는 모두 [MIT License](https://github.com/chick0/to-do/blob/master/LICENSE)를 따르고 있습니다.

단 사용된 Pretendard 폰트의 경우에는 [OFL-1.1](https://github.com/orioncactus/pretendard/blob/main/LICENSE)를 따르고 있습니다.

또 스타일 초기화를 위해 사용하는 minireset.css [MIT License](https://github.com/jgthms/minireset.css/blob/master/LICENSE)를 따르고 있습니다.

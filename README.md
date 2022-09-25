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

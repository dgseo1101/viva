# 비바이노베이션 과제

fastapi를 사용하여 본 과제 코드를 작성하였습니다.
계층형 아키텍처를 사용하였으며, base repository, base service 코드에 crud 를 작업하는 함수들을 구현하고, 
해당 repository, service 코드를 상속받아 사용하는 형태로 하위 repository, service 코드를 구현하였습니다.

1. **프로젝트 설치**
    ```bash
    git clone https://github.com/dgseo1101/viva.git
    cd viva
    ```

2. **의존성 설치 및 env 설정**
    ```bash
    poetry shell
    poetry install

    mkdir _env
    vi _env/dev.env
    ```

3. **데이터베이스 마이그레이션**
    ```bash
    (poetry-shell) alembic revision --autogenerate -m "init"
    (poetry-shell) alembic upgrade head
    ```


4. **도커 빌드 및 서버 실행**
    ```bash
    docker build --tag viva:1.0 -f _docker/Dockerfile . 
    docker run --add-host host.docker.internal:host-gateway -p 8000:8000 viva:1.0

    혹은

    (poetry-shell) python run_server_local.py
    ```

5. **테스트코드 실행**
    ```bash
    pytest -v auth_test.py
    pytest -v notice_test.py
    ```

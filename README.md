# 비바이노베이션 과제

1. **프로젝트 설치**
    ```bash
    git clone 
    cd viva
    ```

2. **의존성 설치 및 env 설정**
    ```bash
    poetry shell
    poetry install

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

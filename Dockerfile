# Python 3.12.5 Alpine 기반 이미지 사용
FROM python:3.12.5-alpine3.19

# 필수 패키지 설치 (빌드 도구 및 psycopg2와 같은 패키지에 필요한 종속성)
RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    libffi-dev \
    build-base \
    linux-headers \
    pcre-dev \
    jpeg-dev \
    zlib-dev \
    gettext \
    bash \
    curl

# 작업 디렉토리 설정
WORKDIR /app

# 시스템에 Redis 설치 (django channels를 위해 Redis가 필요할 수 있음)
RUN apk add --no-cache redis

# Python 패키지 설치에 필요한 pip 및 wheel 최신 버전으로 업데이트
RUN pip install --upgrade pip setuptools wheel

# 프로젝트의 의존성 파일 복사
COPY requirements.txt .

# 의존성 설치
RUN pip install -r requirements.txt

# 소스 코드 복사
COPY .. .

# Redis를 백엔드로 사용하기 위해 환경 변수 설정 (필요시)
#ENV DJANGO_SETTINGS_MODULE=ft_transendence.settings

# 장고 static 파일 수집
RUN python manage.py collectstatic --noinput

# 서버에 사용할 포트 노출
EXPOSE 8000

# Redis 서버 실행, Daphne ASGI 서버 실행
CMD redis-server --daemonize yes && daphne -b 0.0.0.0 -p 8000 ft_transendence.asgi:application

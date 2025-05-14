# Python 3.10 버전의 slim 이미지를 기반으로 사용
FROM python:3.10-slim

# 컨테이너 내부의 작업 디렉토리를 /app으로 설정
# 이후 명령어들은 모두 해당 작업 디렉토리를 기준으로 실행
WORKDIR /app

# 현재 로컬 디렉토리의 requirements.txt 파일을 컨테이너의 /app 디렉토리로 복사
COPY requirements.txt .

# 복사한 requirements.txt 파일을 기반으로 필요한 Python 패키지들을 설치
RUN pip install --no-cache-dir -r requirements.txt

# 현재 로컬 디렉토리의 모든 파일을 컨테이너의 /app 디렉토리로 복사
COPY . .

# 컨테이너가 시작될 때 실행할 기본 명령어를 설정
# Django 서버를 모든 네트워크 인터페이스(0.0.0.0)에서 8000번 포트로 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
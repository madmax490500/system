# 1. 베이스 이미지 설정
FROM python:3.9-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. git 및 기타 필요한 패키지 설치
RUN apt-get update && apt-get install -y git

# 4. 개인 액세스 토큰을 환경 변수로 설정 (빌드 타임 시 비공개 리포지토리에 접근하기 위해)
ARG GIT_TOKEN
ENV GIT_TOKEN=${GIT_TOKEN}

# 5. Git 리포지토리에서 소스코드 가져오기
RUN git clone https://${GIT_TOKEN}@github.com/madmax490500/system.git .

# 6. 필요한 패키지 설치
RUN pip install --no-cache-dir -r /app/system/feed/requirements.txt

# 7. Flask 환경변수 설정
ENV FLASK_APP=/app/feed/app.py

# 8. 컨테이너 포트 설정 (예: 8080)
EXPOSE 8080

# 9. 컨테이너 시작 시 실행할 명령어 (포트 8080 사용)
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]

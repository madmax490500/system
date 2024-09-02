FROM python:3.8

# 필요한 라이브러리 설치
RUN pip install prometheus_client

# 애플리케이션 파일을 컨테이너로 복사
COPY your_application.py /app/

# 작업 디렉토리 설정
WORKDIR /app

# 애플리케이션 실행
CMD ["python", "your_application.py"]

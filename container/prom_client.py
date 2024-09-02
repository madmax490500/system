from prometheus_client import start_http_server, Summary
import random2

# 메트릭을 정의
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

def process_request(t):
    REQUEST_TIME.observe(t)

if __name__ == '__main__':
    # Prometheus 메트릭 엔드포인트를 노출할 HTTP
    start_http_server(8000)
    # 예시로 요청 처리 시간을 기록합니다.
    while True:
        process_request(random2.random())

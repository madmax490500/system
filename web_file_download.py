import os
from datetime import datetime
import requests

# 현재 날짜 가져오기
today = datetime.now().strftime("%Y%m%d")

# 파일 URL 생성
base_url = "https://meditation.su.or.kr/meditation_mp3/2024/"
file_name = f"{today}.mp3"
file_url = base_url + file_name

# 저장할 디렉토리 경로
save_directory = r"d:\temp"

# 디렉토리가 존재하지 않으면 생성
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# 파일 저장 경로
file_path = os.path.join(save_directory, file_name)

# 파일 다운로드
response = requests.get(file_url)
if response.status_code == 200:
    with open(file_path, 'wb') as file:
        file.write(response.content)
    print(f"파일이 성공적으로 다운로드되어 {file_path}에 저장되었습니다.")
else:
    print(f"파일을 다운로드할 수 없습니다. 상태 코드: {response.status_code}")

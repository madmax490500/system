#!/bin/bash

# 복사할 파일
SOURCE_FILE="/home/user/docker-compose.yml"

# 복사할 디렉토리 목록
TARGET_DIRECTORIES=(
    "admin"
    "chat"
    "game"
    "scheduler"
    "shell"
    # 더 많은 디렉토리를 여기에 추가
)

# 파일 복사
for DIR in "${TARGET_DIRECTORIES[@]}"; do
    cp "$SOURCE_FILE" "$DIR"
    echo "Copied $SOURCE_FILE to $DIR"
done

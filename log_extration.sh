#!/bin/bash

START=$(date -d '11 days ago' --iso-8601)
END=$(date -d '1 day ago' --iso-8601)

CURRENT="$START"

while [ "$CURRENT" != "$(date -d "$END +1 day" --iso-8601)" ]; do
    echo $CURRENT

    # 셸 작업 실행
    cat LogStat_${CURRENT}*.log | grep LogIn | uniq | awk -F , '{print $1,$2,$3}' | sort -n -k1 > ${CURRENT}-login.log

    # 날짜 증가
    CURRENT=$(date -d "$CURRENT +1 day" --iso-8601)
done

#UID 추출 자동화 스크립트

#동작방식
#/data/stat/Log/ 에 있는 log 파일 중 -1일에 해당하는 파일의 1-3열 파일을 추출 하여 특정 계정 디렉토리로 보낸다.
#하루씩 날짜.log 형식으로 쌓인다. 운영팀에서 특정 계정으로 SFTP 접속하여 필요한 날짜의 파일을 다운로드 받아 사용한다.
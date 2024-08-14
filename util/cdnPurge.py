#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import requests
import urllib3
import json

usage="""
설명 
    CDN purge를 해주는 python script 입니다.
사용법
    1. ./cdnPurge.py padname emailaddr [ item | wildcad | all ]
    2. padname은 cdn에서 purge할 프로젝트 이름입니다.
    3. emailaddr은 purge 결과를 받을 메일 주소입니다
    4. 'item'은 특정 파일에 대해 purge 할 경우에 사용합니다.
    5. 'wildcard'는 '*'나 '?' 같은 와일드카드 문자를 사용하여 여러개의 파일이니 디렉터리를 purge 할 경우에 사용합니다.
    6. 'all'은 CDN의 전체 파일에 대해 purge 할 경우에 사용합니다.
    7. 'item'이나 'wildcard'의 경우 추가 인자가 필요합니다.
    8. 'all'의 경우 추가 인자가 필요없으며 있을 경우 무시됩니다.
예제
    ./cdnPurge.py shin.COMPANY.co.kr system@COMPANY.co.kr item '/test1.png'
    ./cdnPurge.py shin.COMPANY.co.kr system@COMPANY.co.kr wildcard '/patch/*'
    ./cdnPurge.py shin.COMPANY.co.kr system@COMPANY.co.kr all
"""

# 추가 인자가 없을 경우 사용법을 프린트하고 종료
if len(sys.argv) is 1:
    print(usage)
    sys.exit()

# ssl 관련 warning 제거
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# CDNetworks API URL
url = 'https://openapi.kr.cdnetworks.com/purge/rest/doPurge'

# Purge에 필요한 String Params
params = {}
params['user'] = 'system@COMPANY.co.kr'
params['pass'] = 'PASSWORD'
params['pad'] = sys.argv[1]
params['mailTo'] = sys.argv[2]
params['type'] = sys.argv[3]
params['path'] = sys.argv[4]
params['output'] = 'json'

# GET 방식으로 REST API 호출하고 결과 저장
res = requests.get( url, params=params, verify=False)

print(res.text)
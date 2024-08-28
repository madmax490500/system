# system

## 목적
* 이곳은 공개 가능한 코드를 저장하는 장소 입니다.
* IP, ID, PW 등이 마스킹 또는 변경 처리되기 때문에 그대로 실행하면 에러가 발생합니다.
## 종류
* rocky linux 최초 설치 시 사용
* kernel parameter 변경 (selinux disabled, open files, user 변경) then apply
* 

## 사용법 (다중변수는 스페이스로 구분합니다.)
ansible-playbook main.yml -e "open_file_limit=숫자 limit_user=*"

<hr/>


## 목적
* Ansible 을 이용하여 초기 세팅 (kernel parameter 변경 등)
* AWS EC2 상태변경 (점검, 일괄 stop, 재시작)
* 대량의 conf 변경 (nginx vhost) role base 로 코드 재사용
* Ansible playbook 참고 자료도 첨부


## 사용방법
* ansible-playbook -i 인벤토리 role-플레이북.yml
* 다중변수는 -e 를 사용하고 스페이스로 구분합니다.

## 개선사항
* terraform 과 어떻게 유기적으로 붙일 수 있을지 고민이 필요
* 코드 재활용을 위한 설계 필요
<hr/>


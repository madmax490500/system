## 시작 전 IAM 환경변수가 프로젝트에 맞게 적용되어 있는지 확인
export AWS_PROFILE=프로파일명
aws sts get-caller-identity ## 적용 확인


## Create RDS snapshot

aws rds create-db-snapshot --db-instance-identifier RDSNAME01 --db-snapshot-identifier RDSNAME-snapshot
aws rds create-db-snapshot --db-instance-identifier RDSNAME02 --db-snapshot-identifier RDSNAME-snapshot

## Modify RDS classes
aws rds modify-db-instance --db-instance-identifier RDSNAME01 --db-instance-class db.r4.large --apply-immediately
aws rds modify-db-instance --db-instance-identifier RDSNAME02 --db-instance-class db.r4.large --apply-immediately

## Turn off EC2 for resize
aws ec2 stop-instances --instance-ids EC2NAME
aws ec2 stop-instances --instance-ids EC2NAME

## Modify EC2 
aws ec2 modify-instance-attribute --instance-type=t3.medium --instance-id=EC2NAME
aws ec2 modify-instance-attribute --instance-type=t3.medium --instance-id=EC2NAME


## Check Progress
aws ec2 describe-instances \
--query "Reservations[*].Instances[*].{PublicIP:PublicIpAddress,Type:InstanceType,Name:Tags[?Key=='Name']|[0].Value,Status:State.Name}"  \
--filters "Name=instance-state-name,Values=running" "Name=tag:Name,Values='*'"  \
--output table


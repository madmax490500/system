import boto3

ec2 = boto3.client('ec2', region_name='ap-northeast-2')

instance_id = 'i-09bdbb5fcd607d549'
new_sg_id = 'sg-73c3411b'

# 현재시큐리티그룹확인
response = ec2.describe_instances(InstanceIds=[instance_id])
current_sg_ids = [sg['GroupId'] for sg in response['Reservations'][0]['Instances'][0]['SecurityGroups']]

# 신규시큐리티그룹추가 같은 VPC인지 확인할것
if new_sg_id not in current_sg_ids:
        current_sg_ids.append(new_sg_id)

        # Modify the instance to update the security groups
        ec2.modify_instance_attribute(InstanceId=instance_id, Groups=current_sg_ids)

        print("Security groups updated successfully.")

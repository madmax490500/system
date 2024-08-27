import boto3

ec2 = boto3.client('ec2', region_name='ap-northeast-2')

instance_ids = ['i-123']  # Add more instance ID ['i-123', 'i-456']
new_sg_id = 'sg-123'

for instance_id in instance_ids:
    # 현재 시큐리티 그룹 확인
    response = ec2.describe_instances(InstanceIds=[instance_id])
    current_sg_ids = [sg['GroupId'] for sg in response['Reservations'][0]['Instances'][0]['SecurityGroups']]

    # 신규 시큐리티 그룹 추가, 같은 VPC인지 확인할 것
    if new_sg_id not in current_sg_ids:
        current_sg_ids.append(new_sg_id)

        # Modify the instance to update the security groups
        ec2.modify_instance_attribute(InstanceId=instance_id, Groups=current_sg_ids)

        print(f"Security groups updated successfully for instance {instance_id}.")

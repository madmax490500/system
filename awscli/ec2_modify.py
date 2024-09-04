import boto3
import time

# EC2 define
ec2_client = boto3.client('ec2')

# dictionary
instance_type_mapping = {
    "i-00cb43832fcf5be73": "t3.medium",
    "i-0123456789abcdef0": "t3.small",
    "i-0987654321fedcba0": "t3.medium"
}

# instance modify
for instance_id, instance_type in instance_type_mapping.items():
    try:
        # stop
        print(f"Stopping instance {instance_id}...")
        ec2_client.stop_instances(InstanceIds=[instance_id])
        ec2_client.get_waiter('instance_stopped').wait(InstanceIds=[instance_id])
        print(f"Instance {instance_id} is stopped.")
        
        # modify type
        print(f"Modifying instance {instance_id} to {instance_type}...")
        ec2_client.modify_instance_attribute(
            InstanceId=instance_id,
            InstanceType={'Value': instance_type}
        )
        print(f"Instance {instance_id} updated to {instance_type}.")
        
        # start
        print(f"Starting instance {instance_id}...")
        ec2_client.start_instances(InstanceIds=[instance_id])
        ec2_client.get_waiter('instance_running').wait(InstanceIds=[instance_id])
        print(f"Instance {instance_id} is running.")
        
    except Exception as e:
        print(f"Failed to update instance {instance_id}. Error: {str(e)}")

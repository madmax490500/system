import boto3
import urllib3
import json
from aws_credential import service_key

def get_instance_name(ec2_client, instance_id):
    try:
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        tags = response['Reservations'][0]['Instances'][0]['Tags']
        for tag in tags:
            if tag['Key'] == 'Name':
                return tag['Value']
    except Exception as e:
        print(f"Error fetching instance name for {instance_id}: {e}")
    return "No Name"

def check_ec2_maintenance(service_name, ec2_client, ec2_response):
    if ec2_response['InstanceStatuses']:
        ec2_list = ec2_response['InstanceStatuses']
        for ec2 in ec2_list:
            if 'Events' in ec2:
                instance_id = ec2['InstanceId']
                instance_name = get_instance_name(ec2_client, instance_id)
                az = ec2['AvailabilityZone']
                code = ec2['Events'][0]['Code']
                description = ec2['Events'][0]['Description']
                not_before = ec2['Events'][0]['NotBefore'].strftime("%Y-%m-%d %H:%M:%S %Z")
                instance_state = ec2['InstanceState']['Name']
                result = f'''ServiceName : {service_name}\nAvailabilityZone : {az}\nInstanceId : {instance_id}\nInstanceName : {instance_name}\nInstanceState : {instance_state}\nCode : {code}\nDescription : {description}\nNotBefore : {not_before}'''
                print(result)
                if '[Completed]' not in description:
                    notify_slack(result)
    return

def check_rds_maintenance(service_name, rds_response):
    if rds_response['Events']:
        rds_list = rds_response['Events']
        for rds in rds_list:
            date = rds['Date'].strftime("%Y-%m-%d %H:%M:%S %Z")
            event_categories = rds['EventCategories']
            message = rds['Message']
            source_identifier = rds['SourceIdentifier']
            source_type = rds['SourceType']
            result = f'''ServiceName : {service_name}\nSourceIdentifier : {source_identifier}\nSourceType : {source_type}\nEventCategories : {event_categories}\nDate : {date}\nMessage : {message}'''
            print(result)
            if event_categories != ['notification'] and '[Completed]' not in message:
                notify_slack(result)
    return

def notify_slack(message):
    slack_base_url = 'https://hooks.slack.com/services/'
    slack_url = slack_base_url + 'T6NKZD0U9/B01F32CBYJK/E5yB1fHHzxyApC1Qp5P4qDmA'
    req_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    body, body_channel, body_attachments = {}, {}, {}
    body['attachments'] = []
    body_attachments['color'] = '#AF1AF9'
    body_attachments['pretext'] = 'AWS Maintenance Events'
    body['attachments'].append(body_channel)
    body['attachments'].append(body_attachments)
    body_attachments['text'] = message
    req_body = json.dumps(body).encode('utf-8')
    http = urllib3.PoolManager()
    req = http.request('POST', slack_url, headers=req_headers, body=req_body)
    result = req.data.decode('utf-8')
    return result

def main():
    for key in service_key:
        service_name = key["servicename"]
        access_key_id = key["access_key_id"]
        secret_access_key = key["secret_access_key"]
        regions = key["region"]
        for region in regions:
            session = boto3.session.Session(
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region
            )
            ec2_client = session.client('ec2')
            rds_client = session.client('rds')
            try:
                ec2_response = ec2_client.describe_instance_status()
                check_ec2_maintenance(service_name, ec2_client, ec2_response)
            except Exception as e:
                print(f"Error fetching EC2 instance status: {e}")
            try:
                rds_response = rds_client.describe_events()
                check_rds_maintenance(service_name, rds_response)
            except Exception as e:
                print(f"Error fetching RDS events: {e}")

if __name__ == "__main__":
    main()
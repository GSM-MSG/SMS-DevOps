import boto3
import time

now_hour =  time.localtime().tm_hour

def list_ec2_status(region, now_hour):
    ec2 = boto3.client('ec2', region_name=region)

    response = ec2.describe_instances()

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(f"Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}")
            
            if now_hour < 3:
                if instance['State']['Name'] == 'running':
                    ec2.stop_instances(InstanceIds=[instance['InstanceId']])
            if now_hour > 6:
                if instance['State']['Name'] == 'stopped':
                    ec2.start_instances(InstanceIds=[instance['InstanceId']])

list_ec2_status('ap-northeast-2', now_hour)
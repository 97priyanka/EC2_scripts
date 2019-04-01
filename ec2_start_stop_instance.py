import boto3
from datetime import datetime

def lambda_handler(event, context):
    
    ec2=boto3.client('ec2')
    
    response=ec2.describe_instances(Filters=[{'Name': 'tag-key','Values':['ScheduledShutdown','true']}])
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            for tag in instance["Tags"]:
                state=instance['State']
                now=datetime.now()
                if(tag['Key']=='AutoStartSchedule' and state['Name']=='stopped'):
                    if(tag['Value']==str(now.hour)):
                        ec2.start_instances(InstanceIds=[instance['InstanceId']])
                elif(tag['Key']=='AutoStopSchedule' and state['Name']=='running'):
                    if(tag['Value']==str(now.hour)):
                        ec2.stop_instances(InstanceIds=[instance['InstanceId']])
                    

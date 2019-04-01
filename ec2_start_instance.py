import boto3
from datetime import datetime

def lambda_handler(event, context):
    
    ec2=boto3.client('ec2')
    response=ec2.describe_instances(Filters=[{'Name': 'tag-key','Values':['ScheduledShutdown','true']}])
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            flag=0
            for tag in instance["Tags"]:
                state=instance['State']
                now=datetime.now()
                if(tag['Key']=='AutoStartSchedule' and state['Name']=='stopped'):
                    if(tag['Value']==str(now.hour)):
                        flag=1
                        ec2.start_instances(InstanceIds=[instance['InstanceId']])
            
            if flag==0 :
                print("This instance is in the "+state['Name']+" state and it do not allow auto start schedule.")
                        

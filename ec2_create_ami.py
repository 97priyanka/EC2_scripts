import boto3
from datetime import datetime
from datetime import timedelta

def lambda_handler(event, context):
    
    ec=boto3.client('ec2','us-east-1')
    response = ec.describe_instances(Filters=[{'Name': 'tag-key', 'Values': ['backup','yes']}])

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            for tag in instance["Tags"]:
                if(tag['Key']=='Retention_days'):
                    num_days=int(tag['Value'])
                    deletion_date=str(datetime.date(datetime.now()) + timedelta(days=num_days)) 
                    today=str(datetime.date(datetime.now()))
                    ins_id=instance["InstanceId"]
                    ami=ec.create_image(InstanceId=ins_id,Name='AMI-'+today,Description='AMI for practice')
                    ec.create_tags(Resources=[ami["ImageId"],],Tags=[{'Key': 'Deletion_date','Value': deletion_date},{'Key':'backup','Value':'yes'}])
                    

import boto3
from datetime import datetime

def lambda_handler(event, context):
    
    ec2=boto3.client('ec2','us-east-1')
    now=str(datetime.date(datetime.now()))
    image=ec2.describe_images(Filters=[{'Name':'tag-key','Values':['backup','yes']}])
    for imag in image['Images']:
        for tag in imag['Tags']:
            if tag['Key']=='Deletion_date' and tag['Value']==now :
                image_id=imag['ImageId']
                response = ec2.deregister_image(ImageId=image_id)
                snap=ec2.describe_snapshots(Filters=[{'Name':'description','Values':['*'+image_id+'*']}])
                for snapshot in snap['Snapshots']:
                    ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            else :
                print("No AMI Image with deletion date of today.")
               


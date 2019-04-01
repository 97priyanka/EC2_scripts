import boto3

def lambda_handler(event, context):
    
    ec2 = boto3.client('ec2')
    result = ec2.describe_volumes( Filters=[{'Name': 'tag-key', 'Values': ['backup','yes']}])
        
    for volume in result['Volumes']:
        
        result = ec2.create_snapshot(VolumeId=volume['VolumeId'],Description='Created by Lambda backup function ebs-snapshots')
        
        ec2resource = boto3.resource('ec2', region_name='us-east-1')
        snapshot = ec2resource.Snapshot(result['SnapshotId'])
        
        volumename = 'testSnap'
        
        snapshot.create_tags(Tags=[{'Key': 'Name','Value': volumename}])
        

       

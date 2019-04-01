
import boto3
from botocore.exceptions import ClientError

from datetime import datetime,timedelta

def delete_snapshot(snapshot_id, reg):
    try:  
        ec2resource = boto3.resource('ec2', region_name=reg)
        snapshot = ec2resource.Snapshot(snapshot_id)
        snapshot.delete()
    except ClientError as e:
        print "Caught exception: %s" % e
        
    return
    
def lambda_handler(event, context):
    
    now = datetime.now()
    
    ec2 = boto3.client('ec2', region_name='us-east-1')
        
    result = ec2.describe_snapshots( Filters=[{'Name':'tag-key','Values':['Name','testsnap']}] )
    
    for snapshot in result['Snapshots']:
       
        snapshot_time = snapshot['StartTime'].replace(tzinfo=None)
      
        if (now - snapshot_time) > timedelta(minutes=10):
            delete_snapshot(snapshot['SnapshotId'], 'us-east-1') 

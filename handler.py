import os
import json
import boto3
import urllib
from google.cloud import storage

def s3_to_gcs(event, context):
    s3 = boto3.client("s3")
    if event:
        file_obj = event["Records"][0]
        bucketname = str(file_obj['s3']['bucket']['name'])
        print("From S3 Bucket: ", bucketname)
        filename = str(file_obj['s3']['object']['key'])
        filename = urllib.parse.unquote_plus(filename)
        print("File to be copied: ", filename)
        fileObj = s3.get_object(Bucket = bucketname, Key=filename)
        file_content = fileObj["Body"].read().decode('utf-8')
        
        # Instantiates a GCP storage client
        storage_client = storage.Client()
        gcs_bucket = storage_client.get_bucket(os.environ['GCS_BUCKET_NAME'])
        print("To GCS Bucket: ", os.environ['GCS_BUCKET_NAME'])        
        blob = gcs_bucket.blob(filename)
        blob.upload_from_string(file_content)
        print("Copy successful")
    return 'Done'
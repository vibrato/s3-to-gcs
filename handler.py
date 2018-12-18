import json
import boto3
import urllib

def s3_to_gcs(event, context):
    s3 = boto3.client("s3")
    if event:
        file_obj = event["Records"][0]
        filename = str(file_obj['s3']['object']['key'])
        filename = urllib.parse.unquote_plus(filename)
        print("Filename: ", filename)
        bucketname = str(file_obj['s3']['bucket']['name'])
        fileObj = s3.get_object(Bucket = bucketname, Key=filename)
        file_content = fileObj["Body"].read().decode('utf-8')
        print(file_content)
    return 'Thanks'

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

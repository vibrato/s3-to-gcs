"""
AWS Lambda to copy s3 object from source s3 bucket to Google cloud storage (similar to s3 bucket).
google-cloud-storage package required.

NOTE:
    - Lambda's trigger should be set as source S3 bucket so, any files coming in are notified to Lambda.
    - Environment variables:
        LOG_LEVEL: DEBUG or INFO or ERROR
        GCS_BUCKET_NAME: Google cloud storage bucket (destination bucket)
        GOOGLE_APPLICATION_CREDENTIALS: File name where Google credentials are stored. This file must be
        packaged along with the lambda package.
"""
import os
import logging
import boto3
from StringIO import StringIO
from google.cloud import storage

# Setup logging
LOG = logging.getLogger(__name__)
LOG.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

GCS_BUCKET_NAME=os.environ['GCS_BUCKET_NAME']
S3 = boto3.client('s3')


def lambda_handler(event, context):
    try:
        l_t_bucketKey = _getKeys(event)

        # Create google client
        storage_client = storage.Client()
        gcs_bucket = storage_client.get_bucket(os.environ['GCS_BUCKET_NAME'])

        LOG.debug('About to copy %d files', len(l_t_bucketKey))
        for bucket, key in l_t_bucketKey:
            try:
                inFileObj = StringIO()
                S3.download_fileobj(
                    Bucket=bucket,
                    Key=key,
                    Fileobj=inFileObj
                )
                blob = gcs_bucket.blob(key)
                blob.upload_from_file(inFileObj, rewind=True)  # seek(0) before reading file obj

                LOG.info('Copied s3://%s/%s to gcs://%s/%s', bucket, key, GCS_BUCKET_NAME, key)
            except:
                LOG.exception('Error copying file: {k}'.format(k=key))
        return 'SUCCESS'
    except Exception as e:
        LOG.exception("Lambda function failed:")
        return 'ERROR'


def _getKeys(d_event):
    """
    Extracts (bucket, key) from event

    :param d_event: Event dict
    :return: List of tuples (bucket, key)
    """
    l_t_bucketKey = []
    if d_event:
        if 'Records' in d_event and d_event['Records']:
            for d_record in d_event['Records']:
                try:
                    bucket = d_record['s3']['bucket']['name']
                    key = d_record['s3']['object']['key']
                    l_t_bucketKey.append((bucket, key))
                except:
                    LOG.warn('Error extracting bucket and key from event')
    return l_t_bucketKey

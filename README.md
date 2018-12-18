# S3 to GCS

s3-to-gcs is a lambda function that allows you to perform a one way file copy from an existing Amazon S3 bucket to an existing Google Cloud Storage Bucket.

## Prerequisites

### AWS Setup
1. Create IAM credentials in order to deploy the lambda function by following [this guide](https://serverless.com/framework/docs/providers/aws/guide/credentials/)
2. Ensure that the S3 bucket is created

### Google Cloud Platform setup
1. Create a service account for the lambda function by following [this guide](https://cloud.google.com/iam/docs/creating-managing-service-accounts)
2. Create a set of access keys for the service account by following [this guide](https://cloud.google.com/iam/docs/creating-managing-service-account-keys). Make sure the key type is JSON.
3. Save the access key json file as `service-account.json` in the root folder of this repository
4. Assign "Legacy Bucket Writer" role to the GCS bucket for this service account

## Installation

### Install serverless and dependencies

Install the [serverless](https://serverless.com/) framework by running the following:

```bash
npm install serverless -g
```

Install the other dependencies by running

```bash
npm install
```


### Deploy the lambda function

```bash
# This deploys the lambda function, the IAM role,
sls deploy --aws_bucket <aws_bucket_name> --gcs_bucket <gcs_bucket_name>

# This deploys the S3 event trigger for an existing S3 bucket
sls s3deploy --aws_bucket <aws_bucket_name>
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
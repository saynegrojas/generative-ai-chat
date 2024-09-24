import boto3

def get_s3_client():
    """
    Create and return an S3 client.
    """
    return boto3.client('s3')

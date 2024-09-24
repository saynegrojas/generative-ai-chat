import boto3
import os
from dotenv import load_dotenv

from utils.load_env_variables import load_env_variables

def get_bedrock_client(env_vars):
    env_vars = load_env_variables()
    """
    Create and return a Bedrock client.
    """
    return boto3.client(
        service_name=env_vars['AWS_SERVICE_NAME'],
        region_name=env_vars['AWS_REGION']
    )
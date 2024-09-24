import os
from dotenv import load_dotenv

def load_env_variables():
    load_dotenv()
    return {
        'AWS_REGION': os.getenv('AWS_REGION'),
        'AWS_SERVICE_NAME': os.getenv('AWS_SERVICE_NAME'),
    }
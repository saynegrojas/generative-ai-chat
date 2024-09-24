import os
from dotenv import load_dotenv


def setup_aws_profile():
  load_dotenv()

  aws_profile = os.getenv('AWS_PROFILE')

  if aws_profile:
    os.environ['AWS_PROFILE'] = aws_profile
    print(f'Using AWS profile: {aws_profile}')
  else:
    print('No AWS profile found')
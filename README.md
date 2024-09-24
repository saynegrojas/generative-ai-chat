## A generative ai chat, pdf loader

This application allows you to upload a PDF file to Amazone S3 from the Admin side.
From the User side, and once the PDF file has been uploaded to Amazon S3, it allows you to ask questions regarding the uploaded file.

### Set up AWS:
- Create a bucket in S3 bucket
- Get access to Bedrock models (Titan Embeddings G1 - Text, Anthoropic (Claude v2)) 
- Get access to AWS profile via IAM
- Create IAM user
- Give S3 and Bedrock access to IAM user

- Add IAM access to AWS Profile in code editor


### Run apps:

#### Admin:
- Navigate to Admin
- Go to run_admin.py file and uncomment installation requirements
- execute run_admin.py

### User:
- Navigate to User
- Go to run_app.py file and uncomment installation requirements
- execute run_app.py file

- Note:
  - Once you run the installation requirements once, comment it back to prevent trying to reinstall the packages once more

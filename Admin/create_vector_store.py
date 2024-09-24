import os

from langchain_community.vectorstores import FAISS
from botocore.exceptions import ClientError


def create_vector_store(request_id, documents, bedrock_embeddings, s3_client, bucket_name):
  """
  Create a FAISS vector store from documents, save it locally, and upload to S3.

  Args:
  request_id (str): Unique identifier for the request
  documents (list): List of documents to be vectorized
  bedrock_embeddings: Embedding model to use
  s3_client (boto3.client): Initialized S3 client
  bucket_name (str): Name of the S3 bucket to upload to

  Returns:
  bool: True if the process was successful, False otherwise
  """

  try:
    # Create FAISS index
    vectorstore_faiss = FAISS.from_documents(documents, bedrock_embeddings)

    # Set up file path
    file_name = f'{request_id}.bin'
    folder_path = '/tmp/'

    faiss_path = os.path.join(folder_path, f'{file_name}.faiss')
    pkl_path = os.path.join(folder_path, f'{file_name}.pkl')

    # Save locally
    vectorstore_faiss.save_local(index_name=file_name, folder_path=folder_path)

    # Upload to s3
    s3_client.upload_file(Filename=faiss_path, Bucket=bucket_name, Key='my_faiss.faiss')
    s3_client.upload_file(Filename=pkl_path, Bucket=bucket_name, Key='my_faiss.pkl')

    return True
  except ClientError as e:
    print(f'S3 error occurred: {e}')
    return False
  except Exception as e:
    print(f'An unexpected error occurred: {e}')
    return False
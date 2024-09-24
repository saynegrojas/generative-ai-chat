import os
import boto3
from botocore.exceptions import ClientError

def load_index_from_s3(s3_client, bucket_name, folder_path):
      """
    Download FAISS index files from S3 bucket.

    Args:
    s3_client (boto3.client): Initialized S3 client
    bucket_name (str): Name of the S3 bucket
    folder_path (str): Local folder path to save the downloaded files

    Returns:
    bool: True if both files were downloaded successfully, False otherwise
    """
      
      files_to_download = ['my_faiss.faiss', 'my_faiss.pkl']
      success = True

      for file_name in files_to_download:
            local_file_path = os.path.join(folder_path, file_name)

            try:
              s3_client.download_file(
                Bucket=bucket_name,
                Key=file_name,
                Filename=local_file_path
              )

              print(f'File downloaded successfully to {local_file_path}')

              # Verify file size
              file_size = os.path.getsize(local_file_path)
              print(f'File size: {file_size} bytes')

              if file_size == 0:
                print(f'Warning: {file_name} is empty')
                success = False
            except ClientError as e:
              print(f'Error downloading {file_name}: {e}')
              success = False
            except Exception as e:
              print(f'An unexpected error occurred while downloading: {file_name}: {e}')
              success = False

      return success




# def load_index():
#     try:
#       s3_client.download_file(
#           Bucket=BUCKET_NAME, 
#           Key="my_faiss.faiss", 
#           Filename=f"{folder_path}my_faiss.faiss"
#       )
#       print(f"File downloaded successfully to {folder_path}my_faiss.faiss")
#     except Exception as e:
#       print(f"An error occurred: {e}")
    
#     try:
#       s3_client.download_file(
#           Bucket=BUCKET_NAME, 
#           Key="my_faiss.pkl", 
#           Filename=f"{folder_path}my_faiss.pkl"
#       )
#       print(f"File downloaded successfully to {folder_path}my_faiss.pkl")
#     except Exception as e:
#       print(f"An error occurred: {e}")
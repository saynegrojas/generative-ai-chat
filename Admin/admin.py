import boto3
import streamlit as st
import os
import uuid

from setup_aws_profile import setup_aws_profile

# bedrock
from langchain_community.embeddings import BedrockEmbeddings

# Text Splitter - split text into chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter

# pdf loader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv

# load env
load_dotenv()

BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION')
AWS_SERVICE_NAME = os.getenv('AWS_SERVICE_NAME')
MODEL_ID = os.getenv('MODEL_ID')

# s3 client
s3_client = boto3.client('s3')
bedrock_client = boto3.client(
    service_name=AWS_SERVICE_NAME,
    region_name=AWS_REGION
)

bedrock_embeddings = BedrockEmbeddings(model_id=MODEL_ID, client=bedrock_client)

def get_unique_id():
    return str(uuid.uuid4())

# split the pages into chunks
def split_text(pages, chunk_size, chunk_overlap):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(pages)
  return docs

# create vector and save locally
def create_vector_store(request_id, documents):
  vectorstore_faiss = FAISS.from_documents(documents, bedrock_embeddings)
  file_name = f'{request_id}.bin'
  folder_path = '../temp/'
  vectorstore_faiss.save_local(index_name=file_name, folder_path=folder_path)

  # upload to s3
  s3_client.upload_file(Filename=folder_path + '/' + file_name + '.faiss', Bucket=BUCKET_NAME, Key='my_faiss.faiss')
  s3_client.upload_file(Filename=folder_path + '/' + file_name + '.pkl', Bucket=BUCKET_NAME, Key='my_faiss.pkl')

  return True

def main():
  setup_aws_profile()
  st.write('Admin Site')
  uploader_file = st.file_uploader('Choose a file', 'pdf')

  if uploader_file is not None:
    request_id = get_unique_id()
    st.write(f"Request id: {request_id}")
    saved_file_name = f'{request_id}.pdf'
    with open(saved_file_name, mode='wb') as w:
      # saves file locally
      w.write(uploader_file.getvalue()) 

    loader = PyPDFLoader(saved_file_name)
    pages = loader.load_and_split()

    st.write(f'total pages: {len(pages)}')

    # split text from pdf
    splitted_docs = split_text(pages, 1000, 200)
    st.write(f'splitted docs length: {len(splitted_docs)}')
    st.write('----------------')
    st.write(splitted_docs[0])
    st.write('----------------')
    st.write(splitted_docs[1])

    result = create_vector_store(request_id, splitted_docs)

    if result:
      st.write('PDF processed successfully')
    else:
      st.write('Error: check docs')

if __name__  == '__main__':
  main()
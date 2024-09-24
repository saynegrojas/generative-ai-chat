import streamlit as st
import os
import time

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from split_text import split_text
from create_vector_store import create_vector_store

from utils.setup_aws_profile import setup_aws_profile
from utils.get_s3_client import get_s3_client
from utils.get_bedrock_client import get_bedrock_client
from utils.load_env_variables import load_env_variables
from utils.get_unique_id import get_unique_id

# bedrock
from langchain_community.embeddings import BedrockEmbeddings

# pdf loader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv

# load env
load_dotenv()

# setup aws profile
setup_aws_profile()


BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
MODEL_ID = os.getenv('MODEL_ID')

env_vars = load_env_variables()
s3_client = get_s3_client()
bedrock_client = get_bedrock_client(env_vars)
bedrock_embeddings = BedrockEmbeddings(model_id=MODEL_ID, client=bedrock_client)

def main():
  st.write('Admin Site')
  uploader_file = st.file_uploader('Choose a file', 'pdf')

  if uploader_file is not None:
    request_id = get_unique_id()
    st.write(f"Request id: {request_id}")

    # path to store pdf file
    folder_path = '../temp/'
    saved_file_name = f'{request_id}.pdf'
    full_file_path = os.path.join(folder_path, saved_file_name)
    with open(full_file_path, mode='wb') as w:

      # saves file locally
      w.write(uploader_file.getvalue()) 

    loader = PyPDFLoader(full_file_path)
    pages = loader.load_and_split()

    st.write(f'total pages: {len(pages)}')

    # split text from pdf
    splitted_docs = split_text(pages, 1000, 200)
    st.write(f'splitted docs length: {len(splitted_docs)}')
    st.write('----------------')
    st.write(splitted_docs[0].page_content)
    st.write('----------------')
    st.write(splitted_docs[1].page_content)

    with st.spinner("Processing PDF..."):
      result = create_vector_store(request_id, splitted_docs, bedrock_embeddings, s3_client, BUCKET_NAME)
      if result:
          st.success('PDF processed successfully')
      else:
        st.error('Error: check docs')

if __name__  == '__main__':
  main()
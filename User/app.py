import streamlit as st
import os

from dotenv import load_dotenv

import sys
# checks the directory containing files from other folders
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from load_index_from_s3 import load_index_from_s3
from get_response import get_response
from get_llm import get_llm

from utils.setup_aws_profile import setup_aws_profile
from utils.get_s3_client import get_s3_client
from utils.get_bedrock_client import get_bedrock_client
from utils.load_env_variables import load_env_variables

# bedrock
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS


BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
MODEL_ID = os.getenv('MODEL_ID')
LLM_MODEL_ID = os.getenv('LLM_MODEL_ID')


load_dotenv()
setup_aws_profile()

# get bedrock env to pass in bedrock client
env_vars = load_env_variables()

# s3 client
s3_client = get_s3_client()

# bedrock client
bedrock_client = get_bedrock_client(env_vars)

# bedrock embeddings
bedrock_embeddings = BedrockEmbeddings(model_id=MODEL_ID, client=bedrock_client)

folder_path = '/tmp/'
file_name = 'my_faiss'


def main():
    st.header('Client side')

    # load index from s3
    load_index_from_s3(s3_client, BUCKET_NAME, folder_path)
      
    # create index
    try:
        faiss_index = FAISS.load_local(
            index_name=file_name,
            folder_path = folder_path,
            embeddings=bedrock_embeddings,
            allow_dangerous_deserialization=True,
        )
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    question = st.text_input("Please ask your question")
    if st.button("Ask Question"):
      with st.spinner("Querying..."):

          llm = get_llm(bedrock_client, LLM_MODEL_ID)

          if faiss_index is not None:
            st.write(get_response(llm, faiss_index, question))
            st.success("Done")
          else:
            st.write(f"Failed to load FAISS index  {faiss_index}")


if __name__  == '__main__':
  main()
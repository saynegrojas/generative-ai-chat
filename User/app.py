import boto3
import streamlit as st
import os
import uuid
import pickle

# bedrock
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS

from langchain.llms.bedrock import Bedrock

## prompt and chain
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

os.environ['AWS_PROFILE'] = 'GregBS'

# s3 client
s3_client = boto3.client('s3')
BUCKET_NAME = 'chat-demo1'
bedrock_client = boto3.client(
    service_name = 'bedrock-runtime',
    region_name = 'us-east-1'
)

modelId = 'amazon.titan-embed-text-v1'

bedrock_embeddings = BedrockEmbeddings(model_id=modelId, client=bedrock_client)

folder_path = '../temp/'

# load s3
def load_index():
    try:
      s3_client.download_file(
          Bucket=BUCKET_NAME, 
          Key="my_faiss.faiss", 
          Filename=f"{folder_path}my_faiss.faiss"
      )
      print(f"File downloaded successfully to {folder_path}my_faiss.faiss")
    except Exception as e:
      print(f"An error occurred: {e}")
    
    try:
      s3_client.download_file(
          Bucket=BUCKET_NAME, 
          Key="my_faiss.pkl", 
          Filename=f"{folder_path}my_faiss.pkl"
      )
      print(f"File downloaded successfully to {folder_path}my_faiss.pkl")
    except Exception as e:
      print(f"An error occurred: {e}")

def get_unique_id():
    return str(uuid.uuid4())

def get_llm():
    llm=Bedrock(model_id="anthropic.claude-v2:1", client=bedrock_client,
                model_kwargs={'max_tokens_to_sample': 512})
    return llm


def get_response(llm,vectorstore, question ):
    ## create prompt / template
    prompt_template = """

    Human: Please use the given context to provide concise answer to the question
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    <context>
    {context}
    </context>

    Question: {question}

    Assistant:"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": 5}
    ),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)
    answer=qa({"query":question})
    return answer['result']

def main():
    st.header('Client side')

    load_index()

    # dir_list = os.listdir(folder_path)
    # st.write(f'Files and Dir in {folder_path}')
    # st.write(dir_list)
    with open('../temp/my_faiss.pkl', 'rb') as f:
      data = pickle.load(f)
    print(type(data))
    print(data.keys() if isinstance(data, dict) else "Not a dictionary")
    

    if os.path.exists(f"{folder_path}my_faiss.faiss"):
      print(f"File exists and its size is {os.path.getsize(f'{folder_path}my_faiss.faiss')} bytes")
    else:
      print("File does not exist")

    if os.path.exists(f"{folder_path}my_faiss.pkl"):
      print(f"File exists and its size is {os.path.getsize(f'{folder_path}my_faiss.pkl')} bytes")
    else:
      print("File does not exist")


      
    # create index
    faiss_index = None
    
    try:
        faiss_index = FAISS.load_local(
            index_name="my_faiss",
            folder_path = folder_path,
            embeddings=bedrock_embeddings,
            allow_dangerous_deserialization=True,
        )
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    st.write("INDEX IS READY")
    question = st.text_input("Please ask your question")
    if st.button("Ask Question"):
      with st.spinner("Querying..."):

          llm = get_llm()

          if faiss_index is not None:
            st.write(get_response(llm, faiss_index, question))
            st.success("Done")
          else:
            st.write(f"Failed to load FAISS index  {faiss_index}")


if __name__  == '__main__':
  main()
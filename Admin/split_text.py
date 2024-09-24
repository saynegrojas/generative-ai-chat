# Text Splitter - split text into chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter

# split the pages into chunks
def split_text(pages, chunk_size, chunk_overlap):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(pages)
  return docs
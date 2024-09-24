# bedrock
from langchain.llms.bedrock import Bedrock

def get_llm(bedrock_client, model_id):
    llm = Bedrock(model_id=model_id, client=bedrock_client,
                model_kwargs={'max_tokens_to_sample': 512})
    return llm
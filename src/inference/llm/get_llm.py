import os
import sys

from llm_config import usable


def chk_valid(backend, model) :
    if backend not in usable.keys() :
        raise Exception(f"{backend} backend is not usable")
    if model not in usable.get(backend) :
        raise Exception(f"{backend} backend no have {model}")

def get_model(backend, model) :
    
    chk_valid(backend, model)
    
    if backend == "bedrock" :

        from config.cloud_config import AwsConfig
        from langchain_aws import ChatBedrock

        llm = ChatBedrock(
            model_id=model,
            aws_access_key_id = AwsConfig.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AwsConfig.AWS_SECRET_ACCESS_KEY,
            aws_session_token = AwsConfig.AWS_SESSION_TOKEN,
        )
    
    if backend == "ollama" :

        from langchain_community.chat_models import ChatOllama


        llm = ChatOllama(
            model = model
        )
    
    if backend == "vllm" :

        from langchain_community.llms import VLLMOpenAI

        llm = VLLMOpenAI(
            openai_api_key = "EMPTY",
            openai_api_base = "http://localhost:8000/v1",
            model_name = model,
            # model_kwargs = [{"stop":["."]}],
            # max_token = 2000,
            # temperature = 0.3,
            # top_p = 0.2,
        )
    
    return llm
    

if __name__ == "__main__" :
    backend = "ollama"
    model = "gemma2"
    
    # valid text
    llm = get_llm(backend, model)
    
    # Test
    backend = "ollama"
    model = "gemma2:2b"
    llm = get_llm(backend, model)
    
    llm.invoke("파이썬으로 할 수 있는 재밌는 기능 알려줘")
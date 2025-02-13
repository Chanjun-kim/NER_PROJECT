import os
import sys

from dotenv import load_dotenv
load_dotenv()

PROJECT_ROOT = os.getenv("PROJECT_ROOT")

import numpy as np
import pandas as pd

sys.path.append(PROJECT_ROOT)

from inference.llm.retry_handler import retry_on_failure, async_retry_on_failure


def get_inferencer(model = "gliner") :
    
    if model not in ["gliner", "llm"] :
        raise ValueError(f"{model} is not correct model")
    
    if model.lower().strip() == "gliner" :
        from inference.gliner.inference import Inference
        inferencer = Inference()
        
    elif model.lower().strip() == "llm" :
        from inference.llm.get_llm import get_model
        from inference.llm.inference import StructuredInferencer
        from inference.llm.ner_struct import JK_NER
        llm = get_model(backend = "ollama", model = "qwen2.5:14b")
        inferencer = StructuredInferencer(llm, JK_NER)
        
    return inferencer

        
def gliner_inference(inferencer, text = None) :
        
    from inference.gliner.postprocessor import (
        remove_escape_chars,
        duplicates_suffix,
        split_string,
        remove_nonvalue_keyword,
        remove_private,
        remove_cpn_prefix,
        process_pipeline
    )

    labels = ["회사명", "산업군", "지역", "직업", "직무", "업무", "자격증", "전공", "스킬", "보유기술", "업무도구"]
    _label_map = {"회사명" : "company", "산업군" : "industry", "지역" : "location", "직업" : "job", "직무" : "work", "업무" : "task", "자격증" : "license", "전공" : "major", "스킬" : "skill", "보유기술" : "tech", "업무도구" : "tool"}

    ner = inferencer.extract_ner(text, labels = labels)
    ner.columns = [_label_map[c] for c in ner.columns]

    processing_steps = [
        remove_escape_chars,
        duplicates_suffix,
        split_string,
        remove_nonvalue_keyword,
        remove_private,
        remove_cpn_prefix
    ]


    ner = ner.map(lambda x : process_pipeline(x, processing_steps))
    
    return ner


def llm_inference(inferencer, text) :
    inferencer = retry_on_failure(max_attempts=10, wait_seconds=1)(inferencer.invoke)
    ner = inferencer(text)
    return pd.DataFrame(ner).set_index(0).T


async def allm_inference(inferencer, text) :
    inferencer = async_retry_on_failure(max_attempts=10, wait_seconds=1)(inferencer.invoke)
    ner = await inferencer(text)
    return pd.DataFrame(ner).set_index(0).T


if __name__ == "__main__" :
    text = """
Jobkorea 데이터사이언티스트 모집

LLM 개발자 환영
K8S 환경 경험자 우대
추천 모델링 경력자 최고
검색까지 했으면 금상첨화
"""
    inferencer = get_inferencer()
    gliner_inference(inferencer, text)
    

    inferencer = get_inferencer("llm")
    llm_inference(inferencer, text)

import os
import sys
 
import re
 
import pandas as pd
 
import asyncio

from typing import *

from langchain.output_parsers import PydanticOutputParser, OutputFixingParser

class BaseInference :
    
    def __init__(self, llm) :
        self.llm = llm


class StructuredInferencer(BaseInference) :
    
    def __init__(self, llm, structured) :
        super().__init__(llm)
        
        parser = PydanticOutputParser(pydantic_object = structured)
        fixer = OutputFixingParser.from_llm(parser = parser, llm = llm)
        self.fixer = fixer
        
    def invoke(self, text: str):
        """NER 추출 요청 및 예외 핸들링 (동기)"""
        response = self.fixer.invoke(text)
        return response


    async def ainvoke(self, text: str, semaphore = None) :
        if semaphore :
            async with sem :
                print(text)
                res = await self.fixer.ainvoke(text)
                return res
        else :
            print(text)
            res = await self.fixer.ainvoke(text)
            return res


if __name__ == "__main__" :
    
    import pandas as pd
    
    from get_llm import get_model
    from ner_struct import JK_NER

    llm = get_model("ollama", "qwen2.5:14b")
    
    from dotenv import load_dotenv
    load_dotenv()
    PROJECT_ROOT = os.getenv("PROJECT_ROOT")

    ner_inferencer = StructuredInferencer(llm, JK_NER)

    samples = pd.read_parquet(f"{PROJECT_ROOT}/data/raw/test.parquet")
    sample = samples.content.values[0]
    
    print(ner_inferencer.invoke(sample))
    
#     sem = asyncio.Semaphore(3)
#     tasks = [asyncio.create_task(ner_inferencer.ainvoke(d["content"], sem)) for i, d in samples.iterrows()]
    
#     print(await asyncio.gather(*tasks))

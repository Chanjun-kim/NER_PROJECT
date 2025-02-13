import os
import sys

from functools import reduce

import pandas as pd

from gliner import GLiNER

from dotenv import load_dotenv
load_dotenv()


PROJECT_ROOT = os.getenv("PROJECT_ROOT")
var_cache_dir = f"{os.path.abspath(os.path.join(PROJECT_ROOT, ".."))}/model"

if __name__ == "__main__":
    from textprocessor import chunk_text, preprocess
    sys.path.append(PROJECT_ROOT)    

else :
    from .textprocessor import chunk_text, preprocess


from config.gliner_config import GlinerConfig
model_name = GlinerConfig.model_name


class Inference:
    """
    Handles Named Entity Recognition (NER) and company name extraction using GLiNER model.
    """
    _instance = None
    
    def __new__(cls, model: GLiNER = None):
        if cls._instance is None:
            print(f"Model downloading at {var_cache_dir}")
            cls._instance = super(Inference, cls).__new__(cls)
            cls._instance._model = model or GLiNER.from_pretrained(
                model_name, 
                cache_dir=var_cache_dir
            )
        return cls._instance
    
    def kor_to_eng(self) :
        self._label_map


    def extract_ner(self, text: str, ner_threshold: float = 0.1, labels: list = ["회사명", "산업군", "지역", "직업", "직무", "업무", "자격증", "전공", "스킬", "보유기술", "업무도구"]) -> pd.DataFrame:
        """
        Extract named entities from text.

        Args:
            text (str): Input text.

        Returns:
            pd.DataFrame: DataFrame containing extracted entities.
        """
        labels = labels
        
        try:
            entities = self._model.predict_entities(
                text, labels=labels, threshold=ner_threshold
            )
            if not entities:
                return pd.DataFrame()

            df = pd.DataFrame([[e["text"], e["label"], e["score"]] for e in entities], 
                              columns=["text", "label", "score"])
            df = preprocess(df)
            return df.groupby("label").agg(text=("text", list)).T.reset_index(drop=True)
        
        except Exception as e:
            print(f"Error extracting NER: {e}")
            return pd.DataFrame()


    def extract_cpn_name(self, text: str, length: int = 500, cpn_threshold: float = 0.7) -> str:
        """
        Extract company name from text using the model.

        Args:
            text (str): Input text.
            length (int): Maximum length of input text.

        Returns:
            str: Extracted company name.
        """
        question = "아래의 공고를 올린 회사명은?"
        input_text = question + text[:length]

        try:
            answers = self._model.predict_entities(input_text, ["company_name"], threshold=cpn_threshold)
            if answers:
                df = pd.DataFrame([[e["text"], e["label"], e["score"]] for e in answers], 
                                  columns=["text", "label", "score"])
                return df.sort_values(by=["score"], ascending=False)["text"].iloc[0]
            return ""
        except Exception as e:
            print(f"Error extracting company name: {e}")
            return ""

        
if __name__ == "__main__" :
    model = GLiNER.from_pretrained(
        model_name, 
        cache_dir=var_cache_dir, 
    )
    labels = ["회사명", "산업군", "지역", "직업", "직무", "업무", "자격증", "전공", "스킬", "보유기술", "업무도구 "]
    
    inferencor = Inference()
    
    text = """
토스뱅크 생성형 AI 개발자 모집

담당업무:
AI Agent 개발
RAG 파이프라인 구축 및 모델 개발
대규모 모델 서빙

요구 사항:
Python 상
GPU 관련 경험 우대
    """
    inferencor.extract_ner(text)
    inferencor.extract_cpn_name(text)

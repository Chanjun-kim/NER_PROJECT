import os
import sys

from dotenv import load_dotenv
load_dotenv()

import re

import pandas as pd

PROJECT_ROOT = os.getenv("PROJECT_ROOT")
sys.path.append(PROJECT_ROOT)

from config.file_config import FileConfig


class PreprocessorPipeline:
    
    def __init__(self, file_name, _dir = "data/raw", _format = "parquet", df = None, **kwargs):
        
        self.config = FileConfig
        self.file_name = file_name
        
        if not isinstance(df, pd.DataFrame) :
            _func = eval(f"pd.read_{_format}")
            self.df = _func(f"{PROJECT_ROOT}/{_dir}/{self.file_name}.{_format}", **kwargs)
        else :
            self.df = df

        
    def remove_duplicates(self):
        """텍스트에서 연속된 특수문자를 하나로 줄임"""
        _func = lambda x: re.sub(r"[\s\-\n\t]{2,}", lambda m: m.group(0)[0], str(x))
        self.df["text"] = self.df["text"].apply(_func)
        return self

    
    def get_text_col(self):
        """여러 컬럼을 하나의 텍스트 컬럼으로 결합"""
        text_cols = self.config.text_col[self.file_name]
        self.df["text"] = self.df[text_cols].fillna("").apply(lambda row: "\n".join(row), axis=1)
        return self
    
    
    def available_steps(self):
        """사용 가능한 모든 파이프라인 단계를 반환"""
        return {
            "get_text_col": self.get_text_col,
            "remove_duplicates": self.remove_duplicates,
        }

    
    def list_steps(self):
        """등록된 파이프라인 단계 목록을 출력"""
        print("Available pipeline steps:")
        for step in self.available_steps().keys():
            print(f"- {step}")
        return list(self.available_steps().keys())

    
    def run_pipeline(self, steps=None):
        """
        선택적으로 파이프라인 실행 (지정된 순서 보장).
        
        Args:
            steps (list): 실행할 파이프라인 단계 리스트
        """
        ordered_steps = ["get_text_col", "remove_duplicates"]  # 실행 순서 지정
        available_steps = self.available_steps()

        if steps is None:s
            steps = ordered_steps  # 모든 스텝을 지정된 순서로 실행

        for step in ordered_steps:
            if step in steps and step in available_steps:
                print(f"Running step: {step}")
                available_steps[step]()  # 단계 실행

        return self.df


if __name__ == "__main__" :
    pipeline = PreprocessorPipeline(file_name = "test")
    
    steps = pipeline.list_steps()

    # 특정 파이프라인만 실행
    pipeline.run_pipeline(steps=["get_text_col"])

    # 모든 스텝 실행
    pipeline.run_pipeline(['get_text_col', 'remove_duplicates'])
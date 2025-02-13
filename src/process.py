import os
import sys

from dotenv import load_dotenv
load_dotenv()

PROJECT_ROOT = os.getenv("PROJECT_ROOT")

import numpy as np
import pandas as pd

sys.path.append(PROJECT_ROOT)
from config.file_config import FileConfig

from preprocess import PreprocessorPipeline
from inference.llm.retry_handler import retry_on_failure, async_retry_on_failure
from inferencer import get_inferencer, gliner_inference, llm_inference, allm_inference

def preprocess(file_name, _dir = None, _format = "parquet", df = None, **kwargs) :

    pipeline = PreprocessorPipeline(df = df, file_name=file_name, _format = _format, **kwargs)
    df = pipeline.run_pipeline()
    
    return df


def iteration_inference(df, file_name, model = "gliner") :
    inferencer = get_inferencer(model)
    _inferencer = eval(f"{model}_inference")
    
    key_col = FileConfig.key_col[file_name]
    
    res = [_inferencer(inferencer, r[1]["text"]).assign(**{c : r[1].get(c, "") for c in key_col}) for r in df.iterrows()]
    res = pd.concat(res)
        
    return res


def processor(table, _dir = None, _format = "parquet", model = "gliner", **kwargs) :
    df = preprocess(table, _dir, _format, **kwargs)
    return iteration_inference(df, table, model)


if __name__ == "__main__" :
    # read
    
    df = preprocess(df = None, file_name = None, _format = "parquet", **kwargs)
    iteration_inference(df, table, model)
    # save
    # serve
    

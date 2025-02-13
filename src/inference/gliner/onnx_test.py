import os
import sys

import numpy as np
import pandas as pd

from gliner import GLiNER

import torch
from onnxruntime.quantization import quantize_dynamic, QuantType

from dotenv import load_dotenv
load_dotenv()


PROJECT_ROOT = os.getenv("PROJECT_ROOT")
sys.path.append(PROJECT_ROOT)

from config.gliner_config import GlinerConfig
model_name = GlinerConfig.model_name
var_cache_dir = f"{os.path.abspath(os.path.join(PROJECT_ROOT, ".."))}/model"

save_path = f"{os.path.abspath(os.path.join(PROJECT_ROOT, ".."))}/onnx"
os.makedirs(save_path, exist_ok = True)

onnx_save_path = os.path.join(save_path, "model.onnx")

gliner_model = GLiNER.from_pretrained(
    model_name, 
    cache_dir=var_cache_dir,
    # load_tokenizer=True
)

text = "ONNX is an open-source format designed to enable the interoperability of AI models across various frameworks and tools."
labels = ['format', 'model', 'tool', 'cat']

inputs, _ = gliner_model.prepare_model_inputs([text], labels)

all_inputs =  (inputs['input_ids'], inputs['attention_mask'], 
                inputs['words_mask'], inputs['text_lengths'],
                inputs['span_idx'], inputs['span_mask'])


input_names = ['input_ids', 'attention_mask', 'words_mask', 'text_lengths', 'span_idx', 'span_mask']

dynamic_axes={
    "input_ids": {0: "batch_size", 1: "sequence_length"},
    "attention_mask": {0: "batch_size", 1: "sequence_length"},
    "words_mask": {0: "batch_size", 1: "sequence_length"},
    "text_lengths": {0: "batch_size", 1: "value"},
    "span_idx": {0: "batch_size", 1: "num_spans", 2: "idx"},
    "span_mask": {0: "batch_size", 1: "num_spans"},
    "logits": {0: "batch_size", 1: "sequence_length", 2: "num_spans", 3: "num_classes"},
}

torch.onnx.export(
    gliner_model.model,
    all_inputs,
    input_names=input_names,
    f=onnx_save_path,
    output_names=["logits"],
    dynamic_axes=dynamic_axes,
    opset_version=14,
)


onnx_model = GLiNER.from_pretrained(
    model_name, 
    load_onnx_model=True, 
    onnx_model_file=onnx_save_path
)


text = """
Libretto by Marius Petipa, based on the 1822 novella ``Trilby, ou Le Lutin d'Argail`` by Charles Nodier, first presented by the Ballet of the Moscow Imperial Bolshoi Theatre on January 25/February 6 (Julian/Gregorian calendar dates), 1870, in Moscow with Polina Karpakova as Trilby and Ludiia Geiten as Miranda and restaged by Petipa for the Imperial Ballet at the Imperial Bolshoi Kamenny Theatre on January 17–29, 1871 in St. Petersburg with Adèle Grantzow as Trilby and Lev Ivanov as Count Leopold.
"""


labels = ["person", "book", "location", "date", "actor", "character"]

entities = model.predict_entities(text, labels, threshold=0.4)

for entity in entities:
    print(entity["text"], "=>", entity["label"])


quantized_save_path = os.path.join(save_path, "model_quantized.onnx")

# Quantize the ONNX model
quantize_dynamic(
    onnx_save_path,  # Input model
    quantized_save_path,  # Output model
    weight_type=QuantType.QUInt8  # Quantize weights to 8-bit integers
)

q_model = GLiNER.from_pretrained(
    model_name, 
    load_onnx_model=True, 
    onnx_model_file=quantized_save_path
)

entities = q_model.predict_entities(text, labels, threshold=0.4)

for entity in entities:
    print(entity["text"], "=>", entity["label"])

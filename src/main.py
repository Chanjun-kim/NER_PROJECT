import os
import sys

from process import preprocess, iteration_inference, processor

import argparse

from dotenv import load_dotenv
load_dotenv()

PROJECT_ROOT = os.getenv("PROJECT_ROOT")
sys.path.append(PROJECT_ROOT)


parser = argparse.ArgumentParser()

parser.add_argument("--table", required=True)
parser.add_argument("--model", default = "gliner")
parser.add_argument("--tasks", default = '["preprocess", "iteration_inference"]')

args = parser.parse_args()


table = args.table
model = args.model
tasks = eval(args.tasks)


if __name__ == "__main__" :
    print(processor(table, model = model))


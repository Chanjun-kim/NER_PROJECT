import re

def chunk_text(text, length=500, buffer=32):
    """
    긴 텍스트를 일정 크기의 청크로 분할
    """
    _len = len(text)
    return [text[max(i * length - buffer, 0): (i + 1) * length] for i in range((_len // length) + 1)]


def preprocess(df):
    """
    텍스트 전처리 수행
    """
    df["text"] = df["text"].str.strip()
    df = df[df["text"].str.len() > 0]
    return df
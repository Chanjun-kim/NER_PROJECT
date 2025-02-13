import re

import numpy as np

from functools import reduce


_suffix = ["를", "을", "에", "은", "는", "에서는", "에서", "에는", "합니다", "로", "의", "모집", "분들의", "있고", "이신 분", "입니다", "사원", "과", "이나", "보자", "경력직", "가", "로", "으로", "와", "이나", "경력기술서", "경력증명서", "이", "로써", "로서"]
_sep = [",", "및", "/", "또는", "&", "과 ", "·"]
_nonvaluable = ["핵심역량", "스킬", "자격요건", "경력증명서", "최종합격", "서류전형", "업무능력", "국가보훈대상자", "신체장애인", "직장내괴롭힘", "증명서제출", "당사", "업체", "당사의", "업체의", "주민등록등본", "학력", "기본SKILL", "경력기술서", "이력서", "기본자격", "잡코리아", "당사는", "경험자", "대리", "부사장", "임원면접", "흡연자", "근무", "창사이래", "존공자", "기타", "담당업무", "포지션", "경력", "임원면접", "우대사항", "회사", "", "우대", "자격증", "특이사항", "학자금지원", "애경사지원", "휴가비지원", "복지혜택", "결격사유에해당되지않는자", "숙련자", "", "", "업무", "직원"]

SUFFIX_PATTERN = re.compile(f"({'|'.join(_suffix)})$")
SEP_PATTERN = re.compile(f"({'|'.join(map(re.escape, _sep))})")
PHONENUM_PATTERN = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}\b")
NAME_PATTERN = re.compile(r"(?:[가-힣]{2,3}\s?)?(?:전무|상무|이사|사장|대표|부장|팀장|차장|과장)\s?(?:[가-힣]{2,3})?")
COMPANY_PREFIX = re.compile(r"^\s*(?:㈜|\(주\)|\(유\))\s*")


def remove_escape_chars(lst):
    """공백 및 개행 문자 제거"""
    return [text.strip("\t\n\r ") for text in lst]

def duplicates_suffix(lst) :
    _func = lambda x : re.sub(pattern = SUFFIX_PATTERN, repl = "", string = x)
    return np.unique(lst + [_func(text) for text in lst]).tolist()

def remove_nonvalue_keyword(lst):
    cleaned = [item for item in lst if item not in _nonvaluable and item.strip()]
    return cleaned if cleaned else []

def remove_cpn_prefix(lst) :
    _func = lambda x : re.sub(pattern = COMPANY_PREFIX, repl = "", string = x)
    return [_func(text) for text in lst]

def remove_private(lst):
    """리스트에서 _nonvaluable 및 패턴 매칭 항목 제거"""
    cleaned = [
        item for item in lst 
        if item.strip() and 
           not PHONENUM_PATTERN.search(item) and 
           not NAME_PATTERN.search(item)
    ]
    return cleaned if cleaned else []

def split_string(lst):
    """
    리스트의 문자열을 _sep 목록에 따라 분할하고, 1차원 리스트로 평탄화.
    """
    split_result = []
    for item in lst:
        split_items = [s.strip() for s in SEP_PATTERN.split(item) if s.strip() and not SEP_PATTERN.fullmatch(s)]
        split_result.extend(split_items)  # 중첩 방지 및 평탄화
    return np.unique(lst + split_result).tolist()
    

def process_pipeline(lst, steps):
    """
    리스트 전처리 파이프라인 적용
    """
    return reduce(lambda result, func: func(result), steps, lst)


if __name__ == "__main__" :
    test_data = ["(주)회사", "010-1234-5678", "핵심역량 및 업무", "부장 김철수", "AI 개발", "데이터 분석", "   데이터 AI개발\t\t", "분석을", " 데이터를 ", "\t 회사에서 ", "김철수 부장", "사내데이터/외부데이터"]
    
    processing_steps = [
        remove_escape_chars,
        duplicates_suffix,
        split_string,
        remove_nonvalue_keyword,
        remove_private,
        remove_cpn_prefix
    ]
    
    process_pipeline(test_data, processing_steps)

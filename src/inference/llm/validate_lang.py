import re
from langdetect import detect
ALLOWED_PATTERN = re.compile(r"^[ㄱ-ㅎ가-힣a-zA-Z!@#$%^&*()_+={}\[\]:;\"'<>,.?/~\-|\\ ]+$")

def validate_string(text):
    """입력된 문자열이 허용된 문자만 포함하는지 검증."""
    if not ALLOWED_PATTERN.match(text):
        raise ValueError(f"허용되지 않은 문자가 포함되어 있습니다: {text}")
    return text

def detect_string(text) :
    if detect(text) in ["zh-cn", "ja"] :
        raise ValueError(f"허용되지 않은 언어입니다")
    return text

if __name__ == "__main__" :
    import argparse
    parser = argparse.ArgumentParser()
    
    # 
    parser.add_argument("--test", default = "数据", help = "Data 한자")
    parser.add_argument("--func", default = "validate_string")
    
    args = parser.parse_args("")
    test = args.test
    func = eval(args.func)

    func(test)
    
    # detect_string(test)
    # validate_string(test)

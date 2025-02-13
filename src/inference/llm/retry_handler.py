import asyncio
import logging
import traceback

from tenacity import retry, stop_after_attempt, wait_fixed, RetryError

# 로깅 설정
logging.basicConfig(level=logging.INFO)

def retry_on_failure(max_attempts=3, wait_seconds=3):
    """재시도 로직을 동적으로 설정하고, 에러 발생 시 출력 및 예외 던지기"""

    def decorator(func):
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_fixed(wait_seconds),
            reraise=True,  # 최종 실패 시 예외를 다시 던짐
            after=lambda retry_state: log_exception(retry_state, func),
        )
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_error_details(e, func.__name__)
                # raise  # 예외를 다시 던짐
                return pd.DataFrame()
        return wrapper

    return decorator



def async_retry_on_failure(max_attempts=3, wait_seconds=3):
    """비동기 함수 재시도 데코레이터"""

    def decorator(func):
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_fixed(wait_seconds),
            reraise=True,
            after=lambda retry_state: log_exception(retry_state, func),
        )
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                log_error_details(e, func.__name__)
                # raise
                return pd.DataFrame()
        return wrapper

    return decorator


def log_exception(retry_state, func):
    """재시도 시도 실패 로깅"""
    exception = retry_state.outcome.exception()
    logging.error(f"[ERROR] Function '{func.__name__}' failed at attempt {retry_state.attempt_number} with error: {exception}")


def log_error_details(exception, func_name):
    """에러 상세 정보 로깅"""
    logging.error(f"\n[CRITICAL] Function '{func_name}' failed after all retries.\nException: {exception}")
    logging.error("".join(traceback.format_exc()))  # 전체 스택 트레이스 출력


async def async_unstable_function():
    """비동기 환경에서 실행되는 불안정한 함수"""
    print("Trying to execute...")
    t = random.random()
    if t < 0.8:  # 80% 확률로 실패
        raise ValueError(f"Random failure occurred! {t} is under than 0.8")
    return f"Success! {t} is over than 0.8"


if __name__ == "__main__" :
    import random
    
    def unstable_function():
        print("Trying to execute...")
        t = random.random()
        if t < 0.8:  # 80% 확률로 실패
            raise ValueError(f"Random failure occurred! {t} is under than 0.8")
        return f"Success! {t} is over than 0.8"

    
    retry_text = retry_on_failure(max_attempts=10, wait_seconds=1)(unstable_function)
    
    result = retry_text()
    print("Result:", result)
    

    async def async_unstable_function():
        """비동기 환경에서 실행되는 불안정한 함수"""
        print("Trying to execute...")
        t = random.random()
        if t < 0.8:  # 80% 확률로 실패
            raise ValueError(f"Random failure occurred! {t} is under than 0.8")
        return f"Success! {t} is over than 0.8"


    aretry_text = async_retry_on_failure(max_attempts=10, wait_seconds=1)(async_unstable_function)

    # tasks = [aretry_text() for _ in range(3)]  # 3개의 비동기 작업 병렬 실행
    # results = await asyncio.gather(*tasks, return_exceptions=True)
    # result = retry_text()

import os

class AwsConfig :
    AWS_ACCESS_KEY_ID="..."
    AWS_SECRET_ACCESS_KEY="..."
    AWS_SESSION_TOKEN="..."

    @staticmethod
    def set_env(env):
        """
        환경 변수를 설정하는 정적 메서드.
        
        Args:
            env (str): 설정할 환경 변수 이름 (예: "AWS_ACCESS_KEY")
        
        Raises:
            KeyError: 잘못된 환경 변수를 입력했을 때 예외 발생.
        """
        if hasattr(AwsConfig, env):  # 속성이 존재하는지 확인
            os.environ[env] = getattr(AwsConfig, env)  # 클래스 속성 값을 환경 변수로 설정
            print(f"Environment variable {env} set successfully.")
        else:
            raise KeyError(f"'{env}' is not a valid configuration key.")
    

    @classmethod
    def list_keys(cls):
        """
        설정된 변수(키) 목록을 반환.
        Returns:
            list: 설정된 모든 키 리스트
        """
        return [attr for attr in dir(cls) if not attr.startswith("__") and not callable(getattr(cls, attr))]

    
    @classmethod
    def get(cls, key):
        """
        특정 설정 키의 값을 반환.
        
        Args:
            key (str): 설정 키 이름
        
        Returns:
            str: 해당 설정 키의 값. 키가 없으면 KeyError 발생.
        """
        if hasattr(cls, key):
            return getattr(cls, key)
        else:
            raise KeyError(f"'{key}' is not a valid configuration key.")
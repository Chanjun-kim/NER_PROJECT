class FileConfig:
    """테이블 관련 설정을 관리하는 클래스"""

    file_mapping = {
        "test": "test",
    }

    key_col = {
        "test": ["key"],
    }

    text_col = {
        "test": ["title", "content"],
    }

    updated_col = {
        "test": "reg_dt",
    }
    
    @classmethod
    def get_table_name(cls, key):
        """테이블 이름 가져오기"""
        return cls.table_mapping.get(key, f"Unknown table: {key}")

    @classmethod
    def get_key_columns(cls, key):
        """해당 테이블의 키 컬럼 가져오기"""
        return cls.key_col.get(key, [])

    @classmethod
    def get_text_columns(cls, key):
        """해당 테이블의 텍스트 컬럼 가져오기"""
        return cls.text_col.get(key, [])

    @classmethod
    def list_all_tables(cls):
        """모든 테이블 이름 반환"""
        return list(cls.table_mapping.keys())

    @classmethod
    def table_info(cls, key):
        """테이블 관련 모든 정보를 반환"""
        return {
            "table_name": cls.get_table_name(key),
            "key_columns": cls.get_key_columns(key),
            "text_columns": cls.get_text_columns(key),
            "updated_column": cls.get_updated_column(key),
        }

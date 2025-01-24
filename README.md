# 프로젝트 개요

이 프로젝트는 GLiNER 및 LLM 기반 접근 방식을 사용하여 명명된 엔터티 인식(NER) 및 데이터 전처리를 수행합니다. 이 프로젝트는 데이터 수집, 모델 추론 및 결과 후처리를 지원하도록 구성되었습니다.

## 목차
- [프로젝트 개요](#프로젝트-개요)
- [프로젝트 구조](#프로젝트-구조)
- [설치](#설치)
- [설정](#설정)
- [사용법](#사용법)
- [처리 파이프라인](#처리-파이프라인)
- [스크립트 설명](#스크립트-설명)
- [테스트](#테스트)
- [라이선스](#라이선스)

---

## 프로젝트 구조
```
project/
├── README.md                # 프로젝트 문서
├── config/                   # 설정 파일
│   ├── cloud_config.py        # 클라우드 서비스 설정 (예: AWS)
│   ├── gliner_config.py       # GLiNER 모델 설정
│   ├── project_config.py      # 일반 프로젝트 설정
│   ├── setting.py             # 글로벌 설정 로더
│   └── table_config.py        # 테이블 매핑 설정
├── data/
│   └── raw/                   # 원본 데이터 저장소
│       └── agi.parquet        # 샘플 입력 데이터
├── pyproject.toml             # Poetry 종속성 관리
├── src/                       # 소스 코드
│   ├── inference/             # 추론 모듈
│   │   ├── gliner/             # GLiNER 모델 추론
│   │   │   ├── download_model.py
│   │   │   ├── inference.py
│   │   │   ├── postprocessor.py
│   │   │   └── textprocessor.py
│   │   ├── llm/                # LLM 모델 추론
│   │   │   ├── get_llm.py
│   │   │   ├── inference.py
│   │   │   ├── llm_config.py
│   │   │   └── retry_handler.py
│   ├── inferencer.py          # 통합 추론 핸들러
│   ├── main.py                # 메인 실행 진입점
│   ├── preprocess.py          # 데이터 전처리
│   ├── process.py             # 처리 파이프라인
│   ├── sample.ipynb           # 테스트를 위한 샘플 노트북
└── tests/                     # 유닛 테스트
    └── __init__.py
```

---

## 설치

1. **레포지토리 클론:**
   ```bash
   git clone https://github.com/your_repo.git
   cd project
   ```

2. **종속성 설치:**
   ```bash
   pip install -r requirements.txt
   ```
   Poetry를 사용하는 경우:
   ```bash
   poetry install
   ```

3. **환경 변수 설정:**
   프로젝트 루트에 `.env` 파일 생성 후:
   ```
   PROJECT_ROOT=/absolute/path/to/project
   ```

---

## 설정

프로젝트 설정은 `config/` 디렉토리에서 관리됩니다. 주요 설정 파일:

- `cloud_config.py`: 클라우드 서비스 자격 증명.
- `gliner_config.py`: GLiNER 모델 이름 및 캐시 설정.
- `table_config.py`: 전처리를 위한 테이블 스키마 매핑.

사용 전에 관련 설정 파일을 수정하세요.

---

## 사용법

1. **데이터 처리 파이프라인 실행:**
   ```bash
   python src/main.py --table agi
   ```

2. **전처리 실행:**
   ```bash
   python src/preprocess.py --table agi
   ```

3. **GLiNER 모델 추론 실행:**
   ```bash
   python src/inference/gliner/inference.py --input data/raw/agi.parquet
   ```

---

## 처리 파이프라인

파이프라인은 다음 단계를 포함합니다:

1. **전처리** (`preprocess.py`)
    - 데이터 정제
    - 텍스트 정규화

2. **모델 추론** (`inference.py`)
    - GLiNER 또는 LLM 모델을 사용한 명명된 엔터티 인식(NER)

3. **후처리** (`postprocessor.py`)
    - 엔터티 정리 및 포맷팅

---

## 스크립트 설명

### `src/main.py`
데이터 처리 파이프라인을 실행하는 메인 스크립트.

### `src/preprocess.py`
텍스트 정제 및 토큰화를 수행하는 데이터 전처리.

### `src/inferencer.py`
다양한 모델을 활용한 추론을 관리하는 래퍼.

### `src/inference/gliner/inference.py`
GLiNER 모델을 사용한 NER 추출을 처리.

### `src/inference/llm/inference.py`
GPT 또는 BERT와 같은 LLM 모델을 활용한 추론.

---

## 테스트

유닛 테스트는 `tests/` 디렉토리에 위치합니다.
테스트 실행 방법:

```bash
pytest tests/
```

---

## 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다 - 자세한 내용은 LICENSE 파일을 참조하세요.


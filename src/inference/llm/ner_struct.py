from typing import *
from pydantic import BaseModel, Field

company =  ['컴투스', '씨엔에스', '삼성전자', '삼구아이앤씨', '에치케이씨', '대방건설', '토스', '몽클레르', '하나카드', 'LG유플러스', '농협', '키스템프']
job = ['웹디자이너', '사회복지사', '프론트엔드개발자', '온라인상품기획', '아나운서', '서버엔지니어', '번역가', '방사선사', '양식조리사', '상담원', '재무설계사']
industry = ['정유', '명품수출', '펜션', '학원', '물류센터', '컨설팅', '건설업', '미술교육', '금융', '아웃소싱', '바이오']
exprience =  ['현장생산', '식품제조', '서버구축', '제과생산', '자재정리', '인바운드상담', '백엔드개발', 'AI모델링', '경영관리', '정보보안', '온라인MD']
tool = ['plc', '운전면허', 'CPIM', '영어', '간호조무사', 'Photoshop', 'GA', '직업치료사', 'Kubernetes']
softskill = ['꼼꼼함', '성실함', '부지런함', '적응력']
location = ['서울특별시', '인천 동인구', '미국', '인천 동인구 126-2번지']
 
prompt = f"""해당 공고 및 이력서 텍스트에서 각 컬럼 성격에 맞도록 단어 단위 NER을 추출해
company : 회사 이름 / 예시) {company}
job : 직무명 / 예시) {job}
industry  : 산업명 / 예시) {industry }
exprience : 업무 경험 / 예시) {exprience}
tool : 업무툴 / 예시) {tool}
softskill : 성격 / 예시) {softskill}
location : 위치 / 예시) {location}
"""

class JK_NER(BaseModel):
    f"""{prompt}
"""
    company : List[str] = Field(description=f"company : 회사 이름", examples = company)
    job : List[str] = Field(description=f"job : 직무명", examples = job)
    industry  : List[str] = Field(description=f"industry  : 산업명", examples = industry )
    exprience : List[str] = Field(description=f"exprience : 업무 경험", examples = exprience)
    tool : List[str] = Field(description=f"tool : 업무툴", examples=tool)
    softskill : Optional[List[str]] = Field(description=f"softskill : 성격", examples=softskill)
    location : Optional[List[str]] = Field(description=f"location : 위치", examples=location)


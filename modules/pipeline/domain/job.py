# Job 엔티티(추천 요청 데이터)
# MQ를 통해 전달되는 추천 요청의 핵심 정보를 담는다.

from dataclasses import dataclass

@dataclass
class Job:
    job_id: str            # 작업 식별자
    payload: dict          # 추천에 필요한 데이터
    job_type: str          # 작업 종류(tenant → listing or landlord → tenant)
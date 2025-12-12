# 메시지 DTO 정의
# MQ에서 전달받은 데이터가 유스케이스로 들어갈 수 있도록 DTO를 정의한다.

from pydantic import BaseModel

class JobDTO(BaseModel):
    job_id: str
    request_payload: dict
    job_type: str
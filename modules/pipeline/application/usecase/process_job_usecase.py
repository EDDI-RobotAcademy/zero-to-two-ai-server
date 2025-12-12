# 추천 작업 실행
# 실제 추천 작업 처리 유스케이스를 정의한다.

from ..dto.job_dto import JobDTO
from ..port_in.process_job_port import ProcessJobPort

class ProcessJobUsecase(ProcessJobPort):
    # 여기서는 벡터DB 검색이나 추천 로직을 호출하도록 설계

    async def process(self, job: JobDTO):
        """추천 파이프라인의 핵심 로직을 실행한다."""
        print(f"[Usecase] Processing job {job.job_id}, type={job.job_type}")

        # TODO: 향후 vector DB → 추천 엔진 → 결과 저장 로직 추가
        print(f"[Usecase] payload = {job.payload}")

        return {"status": "done", "job_id": job.job_id}
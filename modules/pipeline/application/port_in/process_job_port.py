# consumer → application 포트
# MQ Consumer가 유스케이스를 호출할 수 있도록 Input Port를 정의한다.

from abc import ABC, abstractmethod
from ..dto.job_dto import JobDTO

class ProcessJobPort(ABC):

    @abstractmethod
    async def process(self, job: JobDTO):
        """수신된 Job을 처리하는 포트"""
        pass
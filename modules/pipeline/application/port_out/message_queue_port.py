# application → producer 포트
# 유스케이스가 MQ에 메시지를 발행할 수 있도록 Output Port를 정의한다.

from abc import ABC, abstractmethod
from ..dto.job_dto import JobDTO

class MessageQueuePort(ABC):

    @abstractmethod
    async def publish(self, job: JobDTO):
        """MQ로 job을 발행하는 인터페이스"""
        pass


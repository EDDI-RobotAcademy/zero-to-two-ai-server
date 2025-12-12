from ..port_in.tenant_recommend_port import TenantRecommendPort
from ..port_out.message_queue_port import MessageQueuePort
from ..port_out.recommend_repository_port import RecommendRepositoryPort

#A → 추천 요청 생성 + 큐 발행 UseCase
class TenantRecommendRequestUseCase(TenantRecommendPort):

    def __init__(self, repo: RecommendRepositoryPort, mq: MessageQueuePort):
        self.repo = repo
        self.mq = mq

    def execute(self, tenant_request_id: int, request_payload: str):
        # 1) 요청 저장
        request_id = self.repo.save_request(tenant_request_id, request_payload)

        # 2) 큐 발행
        self.mq.publish(request_id, request_payload)

        return {
            "request_id": request_id,
            "status": "REQUESTED"
        }
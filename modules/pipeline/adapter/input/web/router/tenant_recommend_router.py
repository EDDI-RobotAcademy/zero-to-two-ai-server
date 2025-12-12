from fastapi import APIRouter
from shared.infrastructure.db.connection import get_connection, release_connection

from modules.pipeline.adapter.output.pg_recommend_repository import PgRecommendRepository
from modules.pipeline.application.usecase.tenant_recommend_request_usecase import TenantRecommendRequestUseCase
from pika import ConnectionParameters, PlainCredentials
from modules.pipeline.adapter.output.rabbitmq_producer import RabbitMQProducer
router = APIRouter()

params = ConnectionParameters(
    host="3.36.64.24",
    port=5672,
    credentials=PlainCredentials("guest", "guest")
)

producer = RabbitMQProducer(
    connection_params=params,
    queue_name="tenant_recommend_request_queue"
)

@router.post("/tenant/recommend")
def recommend(body: dict):
    print("🔥 [ROUTER] /tenant/recommend 요청 도착:", body)

    conn = get_connection()
    try:
        repo = PgRecommendRepository(conn)

        mq = producer

        usecase = TenantRecommendRequestUseCase(repo, mq)

        result = usecase.execute(
            tenant_request_id=body["tenant_request_id"],
            request_payload=body["request_payload"]
        )

        print("✅ [ROUTER] UseCase 결과:", result)
        return result

    finally:
        release_connection(conn)
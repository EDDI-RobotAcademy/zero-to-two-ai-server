# HTTP 요청을 받아 MQ로 Job 메시지를 발행하는 엔드포인트이다.

from fastapi import APIRouter, Body, Query
import uuid
from modules.pipeline.application.dto.job_dto import JobDTO
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

@router.post("/job")
async def create_job(
    payload: dict = Body(..., description="Job payload"),
    job_type: str = Query(..., description="Job type")
):
    """추천 요청을 받아 MQ에 Job 메시지를 발행한다."""
    job_id = str(uuid.uuid4())
    job = JobDTO(job_id=job_id, payload=payload, job_type=job_type)
    await producer.publish(job)
    return {"job_id": job_id, "status": "queued"}

@router.post("/test")
async def test_job():
    return {"status": "ok"}
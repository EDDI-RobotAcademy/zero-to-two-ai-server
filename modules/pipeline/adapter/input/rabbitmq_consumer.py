# 메시지를 받아서 유스케이스 실행
# MQ에서 메시지를 읽어 유스케이스로 전달하는 Consumer Adapter이다.

import json
import pika
from shared.infrastructure.db.connection import get_connection, release_connection
from modules.pipeline.adapter.output.pg_recommend_repository import PgRecommendRepository
from modules.pipeline.application.usecase.tenant_recommend_process_usecase import TenantRecommendProcessUseCase

def callback(ch, method, properties, body):
    data = json.loads(body)
    request_id = data["request_id"]
    payload = data["payload"]

    conn = get_connection()

    try:
        repo = PgRecommendRepository(conn)
        usecase = TenantRecommendProcessUseCase(repo)
        usecase.execute(request_id, payload)

    finally:
        release_connection(conn)

def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='tenant_recommand_request_queue')

    channel.basic_consume(
        queue='tenant_recommand_request_queue',
        on_message_callback=callback,
        auto_ack=True
    )

    print("Worker Started...")
    channel.start_consuming()





# import json
# import aio_pika
# from ...application.usecase.process_job_usecase import ProcessJobUsecase
# from ...application.dto.job_dto import JobDTO
#
# class RabbitMQConsumer:
#
#     def __init__(self, amqp_url: str, queue_name: str):
#         self.amqp_url = amqp_url
#         self.queue_name = queue_name
#         self.usecase = ProcessJobUsecase()  # 유스케이스 주입
#
#     async def start(self):
#         """RabbitMQ에서 메시지를 소비하고 유스케이스로 넘긴다."""
#         connection = await aio_pika.connect_robust(self.amqp_url)
#         channel = await connection.channel()
#         queue = await channel.declare_queue(self.queue_name, durable=True)
#
#         async with connection:
#             async for message in queue:
#                 async with message.process():
#                     print(f"[Consumer] Received message: {message.body}")
#                     data = json.loads(message.body)
#                     job = JobDTO(**data)
#                     await self.usecase.process(job)
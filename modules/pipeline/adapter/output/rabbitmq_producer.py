# 메시지를 MQ로 발행
# Usecase → MQ 로 메시지를 발행하는 Adapter 구현체이다.

import json
import pika

class RabbitMQProducer:

    def __init__(self, connection_params, queue_name):
        self.connection_params = connection_params
        self.queue_name = queue_name

    def publish(self, request_id, payload):
        message_body = json.dumps({
            "request_id": request_id,
            "payload": payload
        })

        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()

        channel.queue_declare(queue=self.queue_name, durable=True)

        channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=message_body,
            properties=pika.BasicProperties(delivery_mode=2)
        )

        print(f"[MQ] message sent: {message_body}")

        connection.close()


# import json
# import aio_pika
# from ...application.port_out.message_queue_port import MessageQueuePort
# from ...application.dto.job_dto import JobDTO


# class RabbitMQProducer(MessageQueuePort):
#
#     def __init__(self, amqp_url: str, queue_name: str):
#         self.amqp_url = amqp_url
#         self.queue_name = queue_name
#
#     async def publish(self, job: JobDTO):
#         """RabbitMQ 큐로 Job 데이터(JSON)를 발행한다."""
#         connection = await aio_pika.connect_robust(self.amqp_url)
#         async with connection:
#             channel = await connection.channel()
#             queue = await channel.declare_queue(self.queue_name, durable=True)
#
#             message = aio_pika.Message(body=json.dumps(job.dict()).encode("utf-8"))
#             await channel.default_exchange.publish(message, routing_key=queue.name)
#
#             print(f"[Producer] Published job {job.job_id}")
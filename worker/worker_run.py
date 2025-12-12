import json
import pika
from shared.infrastructure.db.connection import get_connection, release_connection

from modules.pipeline.adapter.output.pg_recommend_repository import PgRecommendRepository
from modules.pipeline.application.usecase.b_process_usecase import BProcessUseCase

#### 재현님 로직

# MQ 설정
params = pika.ConnectionParameters(
    host="3.36.64.24",
    port=5672,
    credentials=pika.PlainCredentials("guest", "guest")
)

queue_name = "tenant_recommend_request_queue"

def callback(ch, method, properties, body):
    print("🔥 [WORKER] 메시지 수신:", body)

    data = json.loads(body)
    request_id = data["request_id"]
    payload = data["payload"]

    conn = get_connection()
    try:
        repo = PgRecommendRepository(conn)
        b_usecase = BProcessUseCase(repo)

        # 실제 추천 처리 로직 실행
        b_usecase.execute(request_id=request_id, payload=payload)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("✅ [WORKER] 처리 완료:", request_id)

    except Exception as e:
        print("❌ [WORKER] 처리 실패:", e)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    finally:
        release_connection(conn)


def run_worker():
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print("🚀 [WORKER] Consumer 시작")
    channel.start_consuming()


if __name__ == "__main__":
    run_worker()
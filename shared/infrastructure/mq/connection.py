import pika
import os
from dotenv import load_dotenv

load_dotenv()

AMQP_URL = os.getenv("AMQP_URL")

_connection = None
_channel = None

def get_mq_channel():
    global _connection, _channel
    if _connection is None:
        _connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
        _channel = _connection.channel()
    return _channel
import psycopg2
from psycopg2 import pool
from shared.infrastructure.config.settings import settings

_pg_pool = None

def init_pg_pool():
    global _pg_pool
    if _pg_pool is None:
        _pg_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            user=settings.PG_USER,
            password=settings.PG_PASSWORD,
            host=settings.PG_HOST,
            port=settings.PG_PORT,
            database=settings.PG_DATABASE
        )
    return _pg_pool


def get_connection():
    """Use this inside FastAPI or Worker to borrow a connection"""
    if _pg_pool is None:
        init_pg_pool()
    return _pg_pool.getconn()


def release_connection(conn):
    """Return connection to pool"""
    if _pg_pool:
        _pg_pool.putconn(conn)
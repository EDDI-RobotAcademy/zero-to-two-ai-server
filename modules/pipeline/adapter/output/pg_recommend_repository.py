import json
from modules.pipeline.application.port_out.recommend_repository_port import RecommendRepositoryPort

class PgRecommendRepository(RecommendRepositoryPort):

    def __init__(self, conn):
        self.conn = conn

    def save_request(self, tenant_request_id: int, request_payload: str) -> int:
        cur = self.conn.cursor()
        cur.execute("""
                    INSERT INTO tenant_recommend_request (tenant_request_id, request_payload, status)
                    VALUES (%s, %s, 'REQUESTED') RETURNING tenant_recommend_request_id
                    """, (tenant_request_id, request_payload))
        request_id = cur.fetchone()[0]
        self.conn.commit()
        return request_id

    def update_status(self, request_id: int, status: str):
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE tenant_recommend_request
            SET status = %s, updated_at = NOW()
            WHERE id = %s
        """, (status, request_id))
        self.conn.commit()

    def save_result(self, request_id: int, result_json: dict):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO tenant_recommend_result (recommend_request_id, result_json)
            VALUES (%s, %s)
        """, (request_id, json.dumps(result_json)))
        self.conn.commit()
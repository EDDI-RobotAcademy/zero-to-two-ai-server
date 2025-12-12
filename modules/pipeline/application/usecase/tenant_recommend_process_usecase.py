import json

# B → Worker가 실행하는 추천 처리 UseCase
class TenantRecommendProcessUseCase:

    def __init__(self, repo: RecommendRepositoryPort):
        self.repo = repo

    def execute(self, request_id: int, payload: str):
        # 1) PROCESSING 상태 변경
        self.repo.update_status(request_id, "PROCESSING")

        try:
            # 2) 추천 처리 (LLM/RAG)
            result = self.run_rag(payload)

            # 3) 결과 저장
            self.repo.save_result(request_id, result)

            # 4) SUCCESS
            self.repo.update_status(request_id, "SUCCESS")

        except Exception as e:
            self.repo.update_status(request_id, "FAILED")

    def run_rag(self, payload: str):
        # TODO: 실제 RAG 로직 적용
        return {
            "items": [
                {"id": 10, "score": 0.82},
                {"id": 22, "score": 0.71}
            ]
        }
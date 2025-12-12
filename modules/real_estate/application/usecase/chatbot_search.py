from __future__ import annotations

import re
from typing import Sequence

from modules.real_estate.application.dto.chatbot_dto import (
    ChatbotSearchCommand,
    ChatbotSearchListing,
    ChatbotSearchResult,
)
from modules.real_estate.application.dto.embedding_dto import EmbedRequest
from modules.real_estate.application.port_in.chatbot_search_port import ChatbotSearchPort
from modules.real_estate.application.port_out.embedding_port import EmbeddingPort
from modules.real_estate.application.port_out.real_estate_read_port import RealEstateReadPort
from modules.real_estate.application.port_out.real_estate_vector_search_port import (
    RealEstateVectorSearchPort,
    VectorSearchHit,
)


class ChatbotSearchService(ChatbotSearchPort):
    """자연어 메시지를 임베딩 검색으로 연결하는 유스케이스."""

    def __init__(
        self,
        embedder: EmbeddingPort,
        vector_searcher: RealEstateVectorSearchPort,
        estate_reader: RealEstateReadPort,
    ):
        self.embedder = embedder
        self.vector_searcher = vector_searcher
        self.estate_reader = estate_reader

    async def execute(self, cmd: ChatbotSearchCommand) -> ChatbotSearchResult:
        """메시지 → 임베딩 → 벡터 검색 → 매물 DTO 조립."""

        summary_text = self._build_summary(cmd.message)

        if self.embedder.is_dummy():
            # API 키가 없을 때도 프론트에 파싱 결과를 보여주기 위해 빈 결과를 반환
            return ChatbotSearchResult(query=cmd.message, summary=summary_text, results=[])

        embed_requests = [EmbedRequest(record_id=0, text=summary_text)]
        vectors = await self.embedder.embed(embed_requests)

        if not vectors:
            return ChatbotSearchResult(query=cmd.message, summary=summary_text, results=[])

        hits = self.vector_searcher.search(vectors[0].vector, limit=cmd.top_k)
        listings = self._hydrate_listings(hits)
        return ChatbotSearchResult(query=cmd.message, summary=summary_text, results=listings)

    def _build_summary(self, message: str) -> str:
        """챗봇 메시지를 간단히 정제하여 임베딩용 텍스트로 변환."""

        cleaned = re.sub(r"[^0-9a-zA-Z가-힣\s.,;:!?'\"()\\-]", " ", message)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        # 향후 LLM 파서가 추가되면 여기에서 구조화된 텍스트를 생성
        return cleaned

    def _hydrate_listings(self, hits: Sequence[VectorSearchHit]) -> list[ChatbotSearchListing]:
        if not hits:
            return []

        id_order = [hit.real_estate_list_id for hit in hits]
        estate_map = self.estate_reader.fetch_by_ids(id_order)

        enriched = []
        for hit in hits:
            estate = estate_map.get(hit.real_estate_list_id)
            enriched.append(
                ChatbotSearchListing(
                    id=hit.real_estate_list_id,
                    # TODO: 유사 매물 응답값 상세 수정 필요
                    title=getattr(estate, "title", None),
                    address=getattr(estate, "address", None),
                    deal=getattr(estate, "deal", None),
                    deposit=getattr(estate, "deposit", None),
                    cost=getattr(estate, "cost", None),
                    area=getattr(estate, "area", None),
                    room=getattr(estate, "room", None),
                    bath=getattr(estate, "bath", None),
                )
            )
        return enriched
from __future__ import annotations

from modules.real_estate.application.dto.embedding_dto import (
    EmbedRequest,
    EmbedResult,
    SummarizeResult,
)
from modules.real_estate.application.port_in.fetch_and_store_real_estate_port import (
    FetchAndStoreRealEstatePort,
)
from modules.real_estate.application.port_out.embedding_port import EmbeddingPort
from modules.real_estate.application.port_out.real_estate_embedding_port import (
    RealEstateEmbeddingReadPort,
    RealEstateEmbeddingWritePort,
)
from modules.real_estate.application.port_out.summarizer_port import SummarizerPort


class SummarizeAndEmbedAllRealEstateService:
    """전체 매물 요약 및 임베딩 후 pgvector 저장."""

    def __init__(
        self,
        reader: RealEstateEmbeddingReadPort,
        writer: RealEstateEmbeddingWritePort,
        summarizer: SummarizerPort,
        embedder: EmbeddingPort,
    ):
        self.reader = reader
        self.writer = writer
        self.summarizer = summarizer
        self.embedder = embedder

    async def execute(self) -> dict:
        records = self.reader.fetch_all_records()
        print(f"[embed] records fetched: {len(records)}")
        summaries: list[SummarizeResult] = list(self.summarizer.summarize(records))
        print(f"[embed] summaries created: {len(summaries)}")
        embed_requests = [
            EmbedRequest(record_id=s.record_id, text=s.text) for s in summaries
        ]
        if self.embedder.is_dummy():
            print("[embed] OPENAI_API_KEY 미설정: 임베딩/저장 스킵")
            embed_results = []
            saved = 0
        else:
            embed_results: list[EmbedResult] = list(
                await self.embedder.embed(embed_requests)
            )
            print(f"[embed] embeddings created: {len(embed_results)}")
            to_save = [(res.record_id, res.vector) for res in embed_results]
            saved = self.writer.upsert_embeddings(to_save)
        return {
            "total": len(records),
            "summarized": len(summaries),
            "embedded": len(embed_results),
            "saved": saved,
        }

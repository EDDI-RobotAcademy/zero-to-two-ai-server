from __future__ import annotations

import hashlib
import os
from typing import Sequence

import requests

from modules.real_estate.application.dto.embedding_dto import EmbedRequest, EmbedResult
from modules.real_estate.application.port_out.embedding_port import EmbeddingPort


class OpenAIEmbeddingAgent(EmbeddingPort):
    """OpenAI text-embedding-3-small 호출 에이전트. 더미 모드 지원."""

    def __init__(self, api_key: str | None = None, use_dummy: bool = False):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.use_dummy = use_dummy or (self.api_key is None)
        self.model = "text-embedding-3-small"
        self.endpoint = "https://api.openai.com/v1/embeddings"

    def is_dummy(self) -> bool:
        return self.use_dummy

    async def embed(self, requests: Sequence[EmbedRequest]) -> Sequence[EmbedResult]:
        if self.use_dummy:
            return [self._dummy_embed(req) for req in requests]
        texts = [req.text for req in requests]
        resp = await _to_thread(
            requests_post,
            self.endpoint,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={"model": self.model, "input": texts},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        embeds = [item["embedding"] for item in data["data"]]
        return [
            EmbedResult(record_id=req.record_id, vector=vec)
            for req, vec in zip(requests, embeds)
        ]

    def _dummy_embed(self, req: EmbedRequest) -> EmbedResult:
        h = hashlib.sha256(req.text.encode("utf-8")).digest()
        # 32차원 더미 벡터 생성
        vec = [(b - 128) / 128 for b in h[:32]]
        return EmbedResult(record_id=req.record_id, vector=vec)


def requests_post(*args, **kwargs):
    """테스트 시 모킹을 쉽게 하기 위한 래퍼."""
    return requests.post(*args, **kwargs)


async def _to_thread(fn, *args, **kwargs):
    import asyncio

    return await asyncio.to_thread(fn, *args, **kwargs)

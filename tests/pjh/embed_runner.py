"""임베딩 파이프라인 수동 실행 러너 (main과 무관)."""
from __future__ import annotations

import sys
import os
import logging

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from modules.real_estate.application.usecase.summarize_and_embed_all import (
    SummarizeAndEmbedAllRealEstateService,
)
from modules.real_estate.infrastructure.repository.real_estate_embedding_repository import (
    RealEstateEmbeddingRepository,
)
from modules.real_estate.infrastructure.external.summarizers import (
    RuleBasedSummarizer,
)
from modules.real_estate.infrastructure.external.embedding_agent import (
    OpenAIEmbeddingAgent,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    reader_writer = RealEstateEmbeddingRepository()
    summarizer = RuleBasedSummarizer()
    embedder = OpenAIEmbeddingAgent()
    usecase = SummarizeAndEmbedAllRealEstateService(
        reader_writer, reader_writer, summarizer, embedder
    )
    logger.info("임베딩 파이프라인 시작 (더미=%s)", embedder.is_dummy())
    result = usecase.execute()
    logger.info("임베딩 완료: %s", result)
    if embedder.is_dummy():
        logger.warning("임베딩이 더미 모드로 실행되었습니다 (OPENAI_API_KEY 미설정).")


if __name__ == "__main__":
    main()

from __future__ import annotations

from modules.real_estate.application.dto.embedding_dto import EmbedRequest
from modules.real_estate.application.dto.tenant_request_dto import (
    CreateTenantRequestCommand,
    CreateTenantRequestResult,
)
from modules.real_estate.application.port_in.create_tenant_request_port import (
    CreateTenantRequestPort,
)
from modules.real_estate.application.port_out.embedding_port import EmbeddingPort
from modules.real_estate.application.port_out.tenant_request_port import (
    TenantRequestEmbeddingWritePort,
    TenantRequestWritePort,
)
import re


class CreateTenantRequestService(CreateTenantRequestPort):
    """임차인 요청 저장 + 요약/임베딩 후 벡터 DB 저장."""

    def __init__(
        self,
        writer: TenantRequestWritePort,
        embedding_writer: TenantRequestEmbeddingWritePort,
        embedder: EmbeddingPort,
    ):
        self.writer = writer
        self.embedding_writer = embedding_writer
        self.embedder = embedder

    def execute(self, cmd: CreateTenantRequestCommand) -> CreateTenantRequestResult:
        created = self.writer.create_request(cmd)
        print(f"[tenant_request] created id={created.tenant_request_id}")

        if self.embedder.is_dummy():
            # 임베딩 스킵
            print("[tenant_request] OPENAI_API_KEY 미설정: 임베딩 스킵")
            return CreateTenantRequestResult(
                tenant_request_id=created.tenant_request_id, embedded=False
            )

        # 텍스트 빌드 후 요약/임베딩
        summary_text = self._build_text(cmd)
        embed_requests = [
            EmbedRequest(record_id=created.tenant_request_id, text=summary_text)
        ]
        embed_results = self.embedder.embed(embed_requests)
        print(f"[tenant_request] embeddings created: {len(embed_results)}")
        to_save = [(res.record_id, res.vector) for res in embed_results]
        self.embedding_writer.upsert_embeddings(to_save)
        print(f"[tenant_request] embeddings saved: {len(embed_results)}")
        return CreateTenantRequestResult(
            tenant_request_id=created.tenant_request_id, embedded=True
        )

    def _build_text(self, cmd: CreateTenantRequestCommand) -> str:
        parts = []
        if cmd.preferred_area:
            parts.append(f"선호지역: {cmd.preferred_area}")
        if cmd.budget is not None:
            parts.append(f"예산: {cmd.budget}")
        if cmd.family:
            parts.append(f"가족구성: {cmd.family}")
        if cmd.age_range:
            parts.append(f"연령대: {cmd.age_range}")
        if cmd.job:
            parts.append(f"직업: {cmd.job}")
        if cmd.commute_location:
            parts.append(f"출퇴근: {cmd.commute_location}")
        if cmd.car_parking is not None:
            parts.append(f"주차: {'가능' if cmd.car_parking else '불가'}")
        if cmd.pet is not None:
            parts.append(f"반려동물: {'가능' if cmd.pet else '불가'}")
        if cmd.school_district is not None:
            parts.append(f"학군: {'중요' if cmd.school_district else '무관'}")
        if cmd.lifestyle:
            parts.append(f"라이프스타일: {cmd.lifestyle}")
        if cmd.expire_dt:
            parts.append(f"만료일: {cmd.expire_dt}")
        text = "\n".join(parts)
        return self._clean(text)

    def _clean(self, value: str) -> str:
        # 이모지/특수문자 제거, 숫자/한글/영문/기본 문장부호/공백 허용
        text = re.sub(r"[^0-9a-zA-Z가-힣\\s.,;:!?'\"()\\-]", " ", value)
        return re.sub(r"\\s+", " ", text).strip()

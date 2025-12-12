from __future__ import annotations

from modules.real_estate.application.dto.recommendation_dto import (
    RecommendListingsQuery,
    RecommendResult,
    RecommendedListing,
    RecommendedListingDetail,
)
from modules.real_estate.application.port_out.real_estate_embedding_search_port import (
    RealEstateEmbeddingSearchPort,
)
from modules.real_estate.application.port_out.real_estate_read_port import (
    RealEstateReadPort,
)
from modules.real_estate.application.port_out.tenant_request_embedding_port import (
    TenantRequestEmbeddingReadPort,
)


class RecommendRealEstateForTenantService:
    """tenant_request 임베딩 기반 매물 추천."""

    def __init__(
        self,
        tenant_embedding_reader: TenantRequestEmbeddingReadPort,
        real_estate_search: RealEstateEmbeddingSearchPort,
        real_estate_reader: RealEstateReadPort,
    ):
        self.tenant_embedding_reader = tenant_embedding_reader
        self.real_estate_search = real_estate_search
        self.real_estate_reader = real_estate_reader

    async def execute(self, query: RecommendListingsQuery) -> RecommendResult:
        vec = self.tenant_embedding_reader.get_vector(query.tenant_request_id)
        if vec is None:
            return RecommendResult(listings=[])
        search_results = self.real_estate_search.search_similar(
            vec, top_n=query.top_n
        )
        ids = [item_id for item_id, _ in search_results]
        details = {rec.real_estate_list_id: rec for rec in self.real_estate_reader.fetch_by_ids(ids)}
        listings = []
        for item_id, score in search_results:
            rec = details.get(item_id)
            listings.append(
                RecommendedListingDetail(
                    real_estate_list_id=item_id,
                    score=score,
                    title=getattr(rec, "title", None) if rec else None,
                    address=getattr(rec, "address", None) if rec else None,
                    deal_type=getattr(rec, "deal_type", None) if rec else None,
                    deposit=getattr(rec, "deposit", None) if rec else None,
                    rent_fee=getattr(rec, "rent_fee", None) if rec else None,
                    area=getattr(rec, "area", None) if rec else None,
                    residence_type=getattr(rec, "residence_type", None) if rec else None,
                )
            )
        return RecommendResult(listings=listings)

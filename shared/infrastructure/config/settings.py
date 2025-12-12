"""환경 설정 로더 (공용 인프라)."""
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """환경변수를 한곳에서 관리하고 기본값을 부여한다."""

    def __init__(self):
        # 애플리케이션 환경
        self.env = os.environ.get("APP_ENV", "local")

        # DB 설정
        self.PG_HOST = os.getenv("POSTGRES_HOST", "localhost")
        self.PG_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
        self.PG_USER = os.getenv("POSTGRES_USER", "postgres")
        self.PG_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
        self.PG_DATABASE = os.getenv("POSTGRES_DATABASE", "postgres")

        # 크롤링/기타 설정
        self.zigbang_item_ids = self._parse_int_list(os.environ.get("ZIGBANG_ITEM_IDS", ""))
        self.crawl_interval_minutes = int(os.environ.get("CRAWL_INTERVAL_MINUTES", 30))
        self.zigbang_crawl_start_id = self._parse_int(os.environ.get("ZIGBANG_ITEM_CRAWL_START_ID"))
        self.zigbang_crawl_end_id = self._parse_int(os.environ.get("ZIGBANG_ITEM_CRAWL_END_ID"))
        self.zigbang_crawl_regions = self._parse_str_list(os.environ.get("ZIGBANG_ITEM_CRAWL_REGIONS", ""))
        self.zigbang_crawl_round_robin = (
            os.environ.get("ZIGBANG_CRAWL_ROUND_ROBIN", "false").lower() == "true"
        )

    def _parse_int_list(self, raw: str) -> List[int]:
        return [int(x) for x in raw.split(",") if x.strip().isdigit()]

    def _parse_str_list(self, raw: str) -> List[str]:
        return [x.strip() for x in raw.split(",") if x.strip()]

    def _parse_int(self, raw: str | None) -> int | None:
        try:
            return int(raw) if raw is not None else None
        except (TypeError, ValueError):
            return None


def load_settings() -> Settings:
    return Settings()


# 전역 설정 인스턴스 (단순 사용 시 import settings)
settings = load_settings()

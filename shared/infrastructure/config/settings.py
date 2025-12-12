"""Infrastructure settings placeholder (e.g., env parsing)."""
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import List

load_dotenv()

class Settings(BaseSettings):
    PG_HOST: str = os.getenv("PG_HOST")
    PG_PORT: str = os.getenv("PG_PORT")
    PG_USER: str = os.getenv("PG_USER")
    PG_PASSWORD: str = os.getenv("PG_PASSWORD")
    PG_DATABASE: str = os.getenv("PG_DATABASE")
class Settings:
    def __init__(self):
        self.env = os.environ.get("APP_ENV", "local")
        self.zigbang_item_ids = self._parse_int_list(
            os.environ.get("ZIGBANG_ITEM_IDS", "")
        )
        self.crawl_interval_minutes = int(os.environ.get("CRAWL_INTERVAL_MINUTES", 30))
        # 연속 ID 구간 크롤링용
        self.zigbang_crawl_start_id = self._parse_int(os.environ.get("ZIGBANG_ITEM_CRAWL_START_ID"))
        self.zigbang_crawl_end_id = self._parse_int(os.environ.get("ZIGBANG_ITEM_CRAWL_END_ID"))
        self.zigbang_crawl_regions = self._parse_str_list(os.environ.get("ZIGBANG_ITEM_CRAWL_REGIONS", ""))
        # 라운드로빈 모드
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

        # Database 설정
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_DATABASE", "postgres")
        db_user = os.getenv("DB_USERNAME", "postgres")
        db_pass = os.getenv("DB_PASSWORD", "")

        self.DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

settings = Settings()

# class Settings:
#     def __init__(self):
#         self.env = os.environ.get("APP_ENV", "local")
#
#
# def load_settings() -> Settings:
#     return Settings()

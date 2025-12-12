"""직방 매물 크롤링을 주기적으로 실행하는 스크립트.

app/main.py를 건드리지 않고, 테스트 영역에서 독립 실행된다.
"""
from __future__ import annotations

import os
import sys
import logging
import random
import time

# repo 루트를 파이썬 경로에 추가 (tests/ 위치에서 직접 실행될 때 모듈 탐색 보장)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from modules.real_estate.application.dto.fetch_and_store_dto import FetchAndStoreCommand
from modules.real_estate.application.usecase.fetch_and_store_real_estate import (
    FetchAndStoreRealEstateService,
)
from modules.real_estate.infrastructure.api.zigbang_api_client import ZigbangApiClient
from modules.real_estate.infrastructure.repository.real_estate_repository import (
    RealEstateRepository,
)
from shared.infrastructure.config.settings import load_settings
from shared.infrastructure.scheduler.task_scheduler import TaskScheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def build_usecase():
    settings = load_settings()
    zigbang_client = ZigbangApiClient()
    repository = RealEstateRepository()
    usecase = FetchAndStoreRealEstateService(
        zigbang_client,
        repository,
        region_filters=settings.zigbang_crawl_regions,
    )
    return settings, usecase


def run_once(usecase, settings):
    """한 번만 크롤링 → 저장 실행."""
    if settings.zigbang_crawl_start_id and settings.zigbang_crawl_end_id:
        run_range_crawl(usecase, settings)
    else:
        cmd = FetchAndStoreCommand(
            item_ids=settings.zigbang_item_ids or None,
            region=settings.zigbang_region,
            limit=None,
        )
        result = usecase.execute(cmd)
        logger.info(
            "[크롤링] fetched=%s stored=%s skipped=%s errors=%s",
            result.fetched,
            result.stored,
            result.skipped,
            len(result.errors),
        )
        for err in result.errors:
            logger.warning("에러: %s", err)


def run_scheduler():
    settings, usecase = build_usecase()
    scheduler = TaskScheduler()

    run_once(usecase, settings)  # 초기 한 번 실행

    scheduler.add_interval_job(
        func=lambda: run_once(usecase, settings),
        minutes=settings.crawl_interval_minutes,
        job_name="zigbang_crawl",
    )
    scheduler.start()
    logger.info(
        "스케줄러 시작: %s분 간격, item_ids=%s regions=%s",
        settings.crawl_interval_minutes,
        settings.zigbang_item_ids,
        settings.zigbang_crawl_regions
    )
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("스케줄러 종료 요청")
        scheduler.stop()


def chunked(iterable, size):
    buf = []
    for item in iterable:
        buf.append(item)
        if len(buf) >= size:
            yield buf
            buf = []
    if buf:
        yield buf


def run_range_crawl(usecase, settings):
    """연속 ID 범위를 15개 청크로 조회 후 지역 필터링."""
    start_id = settings.zigbang_crawl_start_id
    end_id = settings.zigbang_crawl_end_id
    regions = settings.zigbang_crawl_regions
    if start_id is None or end_id is None:
        logger.error("start_id/end_id가 설정되지 않았습니다.")
        return
    logger.info("[range crawl] start=%s end=%s regions=%s", start_id, end_id, regions)

    all_ids = range(start_id, end_id + 1)
    kept = 0
    fetched = 0
    stored = 0
    errors: list[str] = []

    state = _load_state()
    next_start = state.get("next_start") if settings.zigbang_crawl_round_robin else start_id
    if next_start is None or next_start < start_id or next_start > end_id:
        next_start = start_id

    for chunk in chunked(range(next_start, end_id + 1), 15):
        cmd = FetchAndStoreCommand(item_ids=chunk, region=None, limit=None)
        result = usecase.execute(cmd)
        fetched += result.fetched
        stored += result.stored
        kept += result.stored + result.skipped
        errors.extend(result.errors)
        _save_state(chunk[-1] + 1 if settings.zigbang_crawl_round_robin else start_id)
        time.sleep(random.uniform(3, 7))  # 청크 간 지터 딜레이
        logger.info(
            "[청크] ids=%s..%s fetched=%s stored=%s skipped=%s errors=%s",
            chunk[0],
            chunk[-1],
            result.fetched,
            result.stored,
            result.skipped,
            len(result.errors),
        )

    logger.info(
        "[범위크롤 종료] fetched=%s stored=%s kept=%s errors=%s",
        fetched,
        stored,
        kept,
        len(errors),
    )
    for err in errors:
        logger.warning("에러: %s", err)


def _state_path():
    return os.path.join(CURRENT_DIR, ".crawl_state")


def _load_state():
    path = _state_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return {"next_start": int(content)} if content else {}
    except Exception:
        return {}


def _save_state(next_start: int):
    try:
        with open(_state_path(), "w", encoding="utf-8") as f:
            f.write(str(next_start))
    except Exception:
        logger.warning("상태 저장 실패 next_start=%s", next_start)


if __name__ == "__main__":
    run_scheduler()

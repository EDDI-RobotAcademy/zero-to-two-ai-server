from __future__ import annotations

import logging
import random
import threading
import time
from typing import Callable

import schedule

logger = logging.getLogger(__name__)


class TaskScheduler:
    """schedule 라이브러리를 감싸 백그라운드에서 안전하게 실행."""

    def __init__(self):
        self._scheduler = schedule.Scheduler()
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)

    def add_interval_job(
        self,
        func: Callable,
        minutes: int,
        jitter_seconds: tuple[int, int] = (5, 25),
        job_name: str | None = None,
    ):
        """고정 분 단위 + 지터 적용."""

        def wrapped():
            delay = random.uniform(*jitter_seconds)
            time.sleep(delay)
            try:
                func()
            except Exception as exc:  # noqa: BLE001
                logger.exception("스케줄 작업 실패(%s): %s", job_name or func.__name__, exc)

        self._scheduler.every(minutes).minutes.do(wrapped)

    def _run(self):
        while not self._stop_event.is_set():
            self._scheduler.run_pending()
            time.sleep(1)

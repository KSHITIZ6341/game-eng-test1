
from __future__ import annotations

import logging
import os
from typing import Final

import structlog

_LOG_LEVEL: Final[str] = os.getenv("REAPER_LOG_LEVEL", "INFO").upper()
_IS_JSON: Final[bool] = os.getenv("REAPER_LOG_JSON", "0") == "1"


def _configure() -> structlog.BoundLogger:
    timestamper = structlog.processors.TimeStamper(fmt="iso")
    shared_processors = [timestamper, structlog.processors.StackInfoRenderer(), structlog.processors.format_exc_info]

    if _IS_JSON:
        processors = shared_processors + [structlog.processors.JSONRenderer()]
    else:
        processors = shared_processors + [structlog.dev.ConsoleRenderer()]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, _LOG_LEVEL, logging.INFO)
        ),
        cache_logger_on_first_use=True,
    )
    return structlog.get_logger()


log = _configure()

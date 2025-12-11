# app/core/logging_config.py
import logging
import logging.config
import sys
from app.core.config import get_settings

def configure_logging():
    """
    Configure simple console logging for the app.
    """
    settings = get_settings()
    level = settings.LOG_LEVEL.upper() if settings and settings.LOG_LEVEL else "INFO"

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {"format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"}
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "stream": sys.stdout, "formatter": "default"}
        },
        "root": {"level": level, "handlers": ["console"]},
    }
    logging.config.dictConfig(config)

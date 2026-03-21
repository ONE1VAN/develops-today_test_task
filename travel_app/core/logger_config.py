import os
import logging
from logging.handlers import RotatingFileHandler

from travel_app.core.config import LOG_DIR, LOG_ROTATION_SIZE, LOG_BACKUP_COUNT


def setup_logger(name: str, log_file: str, level=logging.ERROR):
    log_path = os.path.join(LOG_DIR, log_file)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    handler = RotatingFileHandler(
        log_path,
        maxBytes=LOG_ROTATION_SIZE,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8"
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger
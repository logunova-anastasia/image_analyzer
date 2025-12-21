from __future__ import annotations

import json
import logging
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from ..models import ImageFeatures, TransformationRecord  # Нельзя так писать импорты внутри модулей
# Правильно: from src.models import ImageFeatures, TransformationRecord
# Иначе все просто развалится в изолированной среде, например, в докере

DB_PATH = Path('src/database') / 'image_features.sqlite3'
# Лучше "собирать" путь так: `Path('src/database', 'image_features.sqlite3')`
# Чтобы избежать двусмысленного прочтения символа `/`

logger = logging.getLogger(__name__)


def get_connection() -> sqlite3.Connection:
    """
    Создаёт соединение с SQLite, включает foreign_keys и row_factory=Row.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    logger.debug('Ensured database directory exists: %s', DB_PATH.parent)

    logger.info('Opening SQLite connection to %s', DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    logger.debug('SQLite connection established, foreign_keys enabled')
    return conn


@contextmanager
def db_cursor() -> Iterator[sqlite3.Cursor]:
    """
    Контекстный менеджер для работы с курсором.
    """
    conn = get_connection()
    cur = conn.cursor()
    logger.debug('Database cursor created')
    try:
        yield cur
        conn.commit()
        logger.debug('Transaction committed')
    except Exception:
        logger.exception('Error during DB operation, rolling back transaction')
        conn.rollback()
        raise
    finally:
        try:
            cur.close()
            logger.debug('Cursor closed')
        finally:
            conn.close()
            logger.debug('Connection closed')


def init_db() -> None:
    """
    Создаёт таблицы, если их ещё нет.
    """
    logger.info('Initializing database schema (image_features, transformations)')
    with db_cursor() as cur:
        cur.executescript(
            """
            CREATE TABLE IF NOT EXISTS image_features (
                image_id        TEXT PRIMARY KEY,
                width           INTEGER NOT NULL,
                height          INTEGER NOT NULL,
                format          TEXT NOT NULL,
                mean_brightness REAL NOT NULL,
                contrast        REAL NOT NULL,
                density         REAL NOT NULL,
                histogram_json  TEXT NOT NULL,
                computed_at     TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS transformations (
                id           TEXT PRIMARY KEY,
                image_id     TEXT NOT NULL,
                name         TEXT NOT NULL,
                params_json  TEXT NOT NULL,
                applied_at   TEXT NOT NULL,
                FOREIGN KEY(image_id) REFERENCES image_features(image_id) ON DELETE CASCADE
            );
            """
        )
    logger.info('Database schema initialized (or already existed)')


def insert_transformation(record: TransformationRecord) -> None:
    """
    Сохраняет одну запись истории в таблицу transformations.
    """
    logger.info(
        'Inserting transformation: id=%s, image_id=%s, name=%s',
        record.id,
        record.image_id,
        record.name,
    )
    with db_cursor() as cur:
        cur.execute(
            """
            INSERT INTO transformations (
                id, image_id, name, params_json, applied_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                record.id,
                record.image_id,
                str(record.name),
                json.dumps(record.params, ensure_ascii=False),
                record.applied_at.isoformat(),
            ),
        )
    logger.debug('Transformation %s inserted successfully', record.id)


def insert_image_features(features: ImageFeatures) -> None:
    """
    Сохраняет признаки изображения в таблицу image_features.
    """
    logger.info(
        'Inserting image features: image_id=%s, width=%d, height=%d, format=%s',
        features.image_id,
        features.width,
        features.height,
        features.format,
    )
    with db_cursor() as cur:
        cur.execute(
            """
            INSERT INTO image_features (
                image_id,
                width,
                height,
                format,
                mean_brightness,
                contrast,
                density,
                histogram_json,
                computed_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                features.image_id,
                features.width,
                features.height,
                features.format,
                features.mean_brightness,
                features.contrast,
                features.density,
                json.dumps(features.histogram),
                features.computed_at.isoformat(),
            ),
        )
    logger.debug('Image features inserted for image_id=%s', features.image_id)

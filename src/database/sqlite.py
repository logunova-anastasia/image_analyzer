from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from collections.abc import Iterator

from ..models.image import ImageFeatures
from ..models.transformation import TransformationRecord

DB_PATH = Path('src/database') / 'image_features.sqlite3'


def get_connection() -> sqlite3.Connection:
    """
    Создаёт соединение с SQLite, включает foreign_keys и row_factory=Row.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


@contextmanager
def db_cursor() -> Iterator[sqlite3.Cursor]:
    """
    Контекстный менеджер для работы с курсором.
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def init_db() -> None:
    """
    Создаёт таблицы, если их ещё нет.
    """
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


def insert_transformation(record: TransformationRecord) -> None:
    """
    Сохраняет одну запись истории в таблицу transformations.
    """
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


def insert_image_features(features: ImageFeatures) -> None:
    """
    Сохраняет признаки изображения в таблицу image_features.
    """
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

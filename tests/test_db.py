from pathlib import Path

import src.database.sqlite as db


def test_init_db_creates_tables(tmp_path: Path, monkeypatch) -> None:
    """
    Проверка создания таблицы.
    """
    test_db_path = tmp_path / 'test.sqlite3'
    monkeypatch.setattr(db, 'DB_PATH', test_db_path)

    db.init_db()
    assert test_db_path.exists()

    with db.db_cursor() as cur:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cur.fetchall()}

    assert 'image_features' in tables or 'images' in tables

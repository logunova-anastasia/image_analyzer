from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from src.core.io import load_image, save_image


def test_load_png(tmp_path: Path) -> None:
    """
    Проверка загрузки изображений.
    """
    img = Image.new('RGB', (12, 7), color=(1, 2, 3))
    out_path = tmp_path / 'out.png'

    save_image(img, str(out_path))
    assert out_path.exists()
    assert out_path.stat().st_size > 0

    loaded_img, source, data = load_image(str(out_path))

    assert loaded_img.size == (12, 7)
    assert loaded_img.mode == 'RGB'

    assert Path(source.location).resolve() == out_path.resolve()
    assert source.filename == out_path.name

    assert data.source.filename == out_path.name
    assert isinstance(data.history, list)
    assert data.created_at is not None
    assert data.updated_at is None


def test_save_image_creates_directory(tmp_path: Path) -> None:
    """
    Проверка создания директории при сохранении.
    """
    img = Image.new('RGB', (5, 5), color=(10, 20, 30))
    out_path = tmp_path / 'nested' / 'dir' / 'img.png'

    save_image(img, str(out_path))

    assert out_path.exists()
    assert out_path.parent.exists()


def test_load_image_raises_for_missing_file(tmp_path: Path) -> None:
    """
    Проверка создания директории при сохранении.
    """
    missing = tmp_path / 'nope.png'
    with pytest.raises(OSError):
        load_image(str(missing))

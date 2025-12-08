import os
from datetime import datetime

from PIL import Image

from ..models.image import ImageData
from ..models.source import ImageSource


def load_image(path: str) -> tuple[Image.Image, ImageSource, ImageData]:
    """
    Загружает изображение и возвращает (PIL.Image, ImageSource, ImageData).
    """
    img = Image.open(path)

    source = ImageSource(location=os.path.abspath(path), filename=os.path.basename(os.path.abspath(path)))

    data = ImageData(source=source, history=[], created_at=datetime.utcnow(), updated_at=None)

    return img, source, data


def save_image(img: Image.Image, path: str, formatting: str | None = None) -> None:
    """Сохраняет изображение по пути."""
    if formatting is None:
        ext = os.path.splitext(path)[1].lower()
        if ext == '.jpg' or ext == '.jpeg':
            formatting = 'JPEG'
        elif ext == '.png':
            formatting = 'PNG'
        elif ext == '.webp':
            formatting = 'WEBP'
        else:
            formatting = img.format or 'PNG'

    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, format=formatting)

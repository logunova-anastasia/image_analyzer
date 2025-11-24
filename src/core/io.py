from typing import Tuple, Dict, Optional
from PIL import Image
import numpy as np


def load_image(path: str) -> Tuple[Image.Image, Dict]:
    """
    Загружает изображение и возвращает (PIL.Image, meta_dict).
    meta_dict: width, height, format, mode, filesize, path, filename
    """
    pass


def save_image(img: Image.Image, path: str, format: Optional[str] = None) -> None:
    """Сохраняет изображение по пути."""
    pass


def image_to_array(img: Image.Image) -> np.ndarray:
    """Конвертирует PIL.Image в numpy array."""
    pass

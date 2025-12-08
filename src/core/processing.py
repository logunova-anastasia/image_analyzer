from enum import Enum
from typing import Any

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter


def compute_mean_brightness(img: Image.Image) -> float:
    """Вычисляет среднюю яркость (grayscale)."""
    gray = img.convert('L')
    arr = np.asarray(gray, dtype=np.float32)
    return float(arr.mean())


def compute_contrast(img: Image.Image) -> float:
    """Вычисляет контраст (std dev яркости)."""
    gray = img.convert('L')
    arr = np.asarray(gray, dtype=np.float32)
    return float(arr.std())


def compute_edge_density(img: Image.Image) -> float:
    """Оценивает плотность краёв изображения."""
    gray = img.convert('L')
    edges = gray.filter(ImageFilter.FIND_EDGES)

    arr = np.asarray(edges, dtype=np.float32)
    edges_mask = arr > 128
    density = edges_mask.mean()
    return float(density)


class Options(Enum):
    Resize = 1
    Brightness = 2
    Contrast = 3
    Filter = 4


def resize(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Изменение размера изображения."""
    return img.resize(size)


def change_brightness(img: Image.Image, factor: float) -> Image.Image:
    """Изменение яркости (factor: 1.0 = no change)."""
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)


def change_contrast(img: Image.Image, factor: float) -> Image.Image:
    """Изменение контраста."""
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(factor)


def apply_filter(img: Image.Image, params: dict[str, Any]) -> Image.Image:
    """Применяет фильтр (blur, sharpen, edge_enhance и т.п.)."""
    ftype = params.get('type')

    if ftype == 'blur':
        radius = params.get('radius', 2)
        return img.filter(ImageFilter.GaussianBlur(radius))

    elif ftype == 'sharpen':
        return img.filter(ImageFilter.SHARPEN)

    elif ftype == 'edge_enhance':
        return img.filter(ImageFilter.EDGE_ENHANCE)

    elif ftype == 'edges':
        return img.filter(ImageFilter.FIND_EDGES)

    else:
        raise ValueError(f'Unknown filter type: {ftype}')

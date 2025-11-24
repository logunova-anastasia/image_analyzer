from typing import Tuple, Any
from PIL import Image


def compute_mean_brightness(img: Image.Image) -> float:
    """Вычисляет среднюю яркость (grayscale)."""
    pass


def compute_contrast(img: Image.Image) -> float:
    """Вычисляет контраст (std dev яркости)."""
    pass


def compute_edge_density(img: Image.Image) -> float:
    """Оценивает плотность краёв изображения."""
    pass


def resize(img: Image.Image, size: Tuple[int, int]) -> Image.Image:
    """Изменение размера изображения."""
    pass


def change_brightness(img: Image.Image, factor: float) -> Image.Image:
    """Изменение яркости (factor: 1.0 = no change)."""
    pass


def change_contrast(img: Image.Image, factor: float) -> Image.Image:
    """Изменение контраста."""
    pass


def apply_filter(img: Image.Image, filter_name: str, **params: Any) -> Image.Image:
    """Применяет фильтр (blur, sharpen, edge_enhance и т.п.)."""
    pass

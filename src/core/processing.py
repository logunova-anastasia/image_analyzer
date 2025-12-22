import logging
from enum import Enum

import numpy as np
from numpy.typing import NDArray
from PIL import Image, ImageEnhance, ImageFilter

logger = logging.getLogger(__name__)


# Докстринги неполные - нет описания параметров и ретерна
def compute_mean_brightness(img: Image.Image) -> float:
    """Вычисляет среднюю яркость (grayscale)."""
    logger.debug(
        'Computing mean brightness: size=%s, mode=%s',
        getattr(img, 'size', None),
        getattr(img, 'mode', None),
    )
    arr: NDArray[np.float32] = np.asarray(img.convert('L'), dtype=np.float32)
    mean_value = float(arr.mean())
    logger.debug('Mean brightness computed: %f', mean_value)
    return mean_value


def compute_contrast(img: Image.Image) -> float:
    """Вычисляет контраст (std dev яркости)."""
    logger.debug(
        'Computing contrast: size=%s, mode=%s',
        getattr(img, 'size', None),
        getattr(img, 'mode', None),
    )
    arr: NDArray[np.float32] = np.asarray(img.convert('L'), dtype=np.float32)
    contrast_value = float(arr.std())
    logger.debug('Contrast computed: %f', contrast_value)
    return contrast_value


def compute_edge_density(img: Image.Image) -> float:
    """Оценивает плотность краёв изображения."""
    logger.debug(
        'Computing edge density: size=%s, mode=%s',
        getattr(img, 'size', None),
        getattr(img, 'mode', None),
    )

    arr: NDArray[np.float32] = np.asarray(img.convert('L').filter(ImageFilter.FIND_EDGES), dtype=np.float32)
    edges_mask = arr > 128
    density = float(edges_mask.mean())
    logger.debug('Edge density computed: %f', density)
    return density


# Enum-ы лучше унести в отдельный файл
class Options(Enum):
    Resize = 1
    Brightness = 2
    Contrast = 3
    Filter = 4


def resize(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Изменение размера изображения."""
    logger.debug('Resizing image from %s to %s', getattr(img, 'size', None), size)
    result = img.resize(size)
    logger.debug('Image resized: new_size=%s', getattr(result, 'size', None))
    return result


def change_brightness(img: Image.Image, factor: float) -> Image.Image:
    """Изменение яркости (factor: 1.0 = no change)."""
    logger.debug('Changing brightness with factor=%s', factor)
    enhancer = ImageEnhance.Brightness(img)
    result = enhancer.enhance(factor)
    logger.debug('Brightness changed with factor=%s', factor)
    return result


def change_contrast(img: Image.Image, factor: float) -> Image.Image:
    """Изменение контраста."""
    logger.debug('Changing contrast with factor=%s', factor)
    enhancer = ImageEnhance.Contrast(img)
    result = enhancer.enhance(factor)
    logger.debug('Contrast changed with factor=%s', factor)
    return result


def apply_filter(img: Image.Image, ftype: str) -> Image.Image:
    """Применяет фильтр (blur, sharpen, edge_enhance и т.п.)."""
    logger.debug('Applying filter: type=%s, params=%r', ftype)

    if ftype == 'blur':
        logger.debug('Applying GaussianBlur with radius=%s', 10)
        result = img.filter(ImageFilter.GaussianBlur(10))

    elif ftype == 'sharpen':
        logger.debug('Applying SHARPEN filter')
        result = img.filter(ImageFilter.SHARPEN)

    elif ftype == 'edge_enhance':
        logger.debug('Applying EDGE_ENHANCE filter')
        result = img.filter(ImageFilter.EDGE_ENHANCE)

    elif ftype == 'edges':
        logger.debug('Applying FIND_EDGES filter')
        result = img.filter(ImageFilter.FIND_EDGES)

    else:
        logger.error('Unknown filter type: %s', ftype)
        raise ValueError(f'Unknown filter type: {ftype}')

    logger.debug('Filter %s applied successfully', ftype)
    return result

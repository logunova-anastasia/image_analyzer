import numpy as np
import pytest
from PIL import Image


@pytest.fixture
def gray_image_10x10() -> Image.Image:
    """
    Изображение 10x10, цвет 128.
    """
    return Image.new('L', (10, 10), color=128)


@pytest.fixture
def rgb_image_10x10() -> Image.Image:
    """
    Изображение 10x10, цвет RGB (10, 20, 30).
    """
    return Image.new('RGB', (10, 10), color=(10, 20, 30))


@pytest.fixture
def edge_image_10x10() -> Image.Image:
    """
    Изображение с черной и белой половинами.
    """
    arr = np.zeros((10, 10), dtype=np.uint8)
    arr[:, 5:] = 255
    return Image.fromarray(arr, mode='L')

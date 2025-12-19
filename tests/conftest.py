import numpy as np
import pytest
from PIL import Image


@pytest.fixture
def gray_image_10x10() -> Image.Image:
    # 10x10, серый 128
    return Image.new('L', (10, 10), color=128)


@pytest.fixture
def rgb_image_10x10() -> Image.Image:
    # 10x10, RGB (10, 20, 30)
    return Image.new('RGB', (10, 10), color=(10, 20, 30))


@pytest.fixture
def edge_image_10x10() -> Image.Image:
    # Половина чёрная, половина белая -> чёткий вертикальный край
    arr = np.zeros((10, 10), dtype=np.uint8)
    arr[:, 5:] = 255
    return Image.fromarray(arr, mode='L')

import numpy as np
import pytest
from PIL import Image

from src.core.processing import (
    resize,
    change_brightness,
    change_contrast,
    compute_mean_brightness,
    compute_contrast,
    compute_edge_density,
)


def test_resize_changes_size(gray_image_10x10: Image.Image) -> None:
    out = resize(gray_image_10x10, (20, 5))
    assert out.size == (20, 5)
    assert out.mode == gray_image_10x10.mode


def test_change_brightness_increases_mean(gray_image_10x10: Image.Image) -> None:
    before = compute_mean_brightness(gray_image_10x10)
    out = change_brightness(gray_image_10x10, 1.2)
    after = compute_mean_brightness(out)
    assert after > before


def test_change_brightness_decreases_mean(gray_image_10x10: Image.Image) -> None:
    before = compute_mean_brightness(gray_image_10x10)
    out = change_brightness(gray_image_10x10, 0.8)
    after = compute_mean_brightness(out)
    assert after < before


def test_change_contrast_constant_image_stays_constant(gray_image_10x10: Image.Image) -> None:
    # На полностью однотонном изображении контраст = 0, и после усиления контраста
    # оно должно остаться однотонным (или почти однотонным, но в PIL обычно ровно).
    out = change_contrast(gray_image_10x10, 2.0)
    arr = np.asarray(out)
    assert arr.min() == arr.max()


def test_compute_mean_brightness_known_value(gray_image_10x10: Image.Image) -> None:
    val = compute_mean_brightness(gray_image_10x10)
    assert pytest.approx(val, abs=1e-6) == 128.0


def test_compute_contrast_zero_for_constant(gray_image_10x10: Image.Image) -> None:
    c = compute_contrast(gray_image_10x10)
    assert pytest.approx(c, abs=1e-6) == 0.0


def test_compute_edge_density_higher_for_edge(edge_image_10x10: Image.Image, gray_image_10x10: Image.Image) -> None:
    # На картинке с резким краем плотность границ должна быть выше, чем на однотонной
    edge_density = compute_edge_density(edge_image_10x10)
    flat_density = compute_edge_density(gray_image_10x10)
    assert edge_density > flat_density

from datetime import datetime
from typing import Any
from uuid import uuid4

from PIL import Image

from ..core.processing import (
    Options,
    apply_filter,
    change_brightness,
    change_contrast,
    compute_contrast,
    compute_edge_density,
    compute_mean_brightness,
    resize,
)
from ..database.sqlite import insert_image_features, insert_transformation
from ..models.image import ImageData, ImageFeatures
from ..models.transformation import TransformationRecord


def apply_operation(
    img: Image.Image, data: ImageData, op: dict[Options, Any], image_id: str
) -> tuple[Image.Image, TransformationRecord]:
    """
    Применяет одну операцию (op: {'name':..., 'params':{...}}) и возвращает новое изображение и запись об изменении.
    """
    result = img
    record: TransformationRecord | None = None

    for key, value in op.items():
        if key == Options.Resize:
            result = resize(img, value)
        elif key == Options.Brightness:
            result = change_brightness(img, float(value))
        elif key == Options.Contrast:
            result = change_contrast(img, value)
        elif key == Options.Filter:
            result = apply_filter(img, value)
        else:
            raise AttributeError('Wrong argument. Available options are: Resize, Brightness, Contrast, Filter.')

        record = TransformationRecord(
            id=str(uuid4()),
            image_id=image_id,
            name=key,
            params=value,
            applied_at=datetime.utcnow(),
        )

        data.updated_at = datetime.utcnow()
        data.history.append(record)

        insert_transformation(record)

    if record is None:
        raise ValueError('No operations provided for apply_operation().')

    return result, record


def analyze(img: Image.Image, image_id: str) -> ImageFeatures:
    """
    Анализирует изображение и возвращает словарь с полученными значениями.
    """
    width, height = img.size
    fmt = str(getattr(img, 'format', None))

    gray = img.convert('L')
    histogram = gray.histogram()

    analysis = ImageFeatures(
        id=str(uuid4()),
        image_id=image_id,
        width=width,
        height=height,
        format=fmt,
        mean_brightness=compute_mean_brightness(img),
        contrast=compute_contrast(img),
        density=compute_edge_density(img),
        histogram=histogram,
    )

    insert_image_features(analysis)

    return analysis

import logging
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
from ..database import insert_image_features, insert_transformation
from ..models import ImageData, ImageFeatures, TransformationRecord

logger = logging.getLogger(__name__)


def apply_operation(
    img: Image.Image, data: ImageData, op: dict[Options, Any], image_id: str
) -> tuple[Image.Image, TransformationRecord]:
    """
    Применяет одну операцию (op: {'name':..., 'params':{...}}) и возвращает новое изображение и запись об изменении.
    """
    logger.info('Applying operation(s) to image %s', image_id)
    logger.debug('Incoming operations: %r', op)

    result = img
    record: TransformationRecord | None = None

    for key, value in op.items():
        logger.debug('Processing operation: %s with params=%r', key, value)

        if key == Options.Resize:
            logger.debug('Resizing image from %s with size=%r', getattr(result, 'size', None), value)
            result = resize(img, tuple(value))
            logger.debug('Image resized, new size=%s', getattr(result, 'size', None))

        elif key == Options.Brightness:
            logger.debug('Changing brightness with factor=%s', value)
            result = change_brightness(img, float(value))

        elif key == Options.Contrast:
            logger.debug('Changing contrast with factor=%s', value)
            result = change_contrast(img, float(value))

        elif key == Options.Filter:
            logger.debug('Applying filter with params=%r', value)
            result = apply_filter(img, value)

        else:
            logger.error(
                'Wrong argument for apply_operation: %r. Available options: Resize, Brightness, Contrast, Filter.',
                key,
            )
            raise AttributeError('Wrong argument. Available options are: Resize, Brightness, Contrast, Filter.')

        record = TransformationRecord(
            id=str(uuid4()),
            image_id=image_id,
            name=key,
            params=value,
            applied_at=datetime.utcnow(),
        )
        logger.debug('TransformationRecord created: %r', record)

        data.updated_at = datetime.utcnow()
        data.history.append(record)
        logger.debug('ImageData updated_at=%s, history length=%d', data.updated_at, len(data.history))

        insert_transformation(record)
        logger.info('Transformation %s for image %s inserted into database', key, image_id)

    if record is None:
        logger.error('No operations provided for apply_operation() for image %s', image_id)
        raise ValueError('No operations provided for apply_operation().')

    logger.info('Operation(s) applied successfully to image %s', image_id)
    return result, record


def analyze(img: Image.Image, image_id: str) -> ImageFeatures:
    """
    Анализирует изображение и возвращает словарь с полученными значениями.
    """
    logger.info('Analyzing image %s', image_id)

    width, height = img.size
    fmt = str(getattr(img, 'format', None))
    logger.debug('Image basic info: width=%d, height=%d, format=%s', width, height, fmt)

    gray = img.convert('L')
    histogram = gray.histogram()
    logger.debug('Histogram length: %d', len(histogram))

    mean_brightness = compute_mean_brightness(img)
    contrast = compute_contrast(img)
    density = compute_edge_density(img)

    logger.debug(
        'Computed features for %s: mean_brightness=%f, contrast=%f, edge_density=%f',
        image_id,
        mean_brightness,
        contrast,
        density,
    )

    analysis = ImageFeatures(
        id=str(uuid4()),
        image_id=image_id,
        width=width,
        height=height,
        format=fmt,
        mean_brightness=mean_brightness,
        contrast=contrast,
        density=density,
        histogram=histogram,
    )

    insert_image_features(analysis)
    logger.info('Image features inserted into database for image %s (features_id=%s)', image_id, analysis.id)

    return analysis

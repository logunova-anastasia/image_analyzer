from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from ..models.source import ImageSource
from ..models.transformation import TransformationRecord


@dataclass
class ImageData:
    """
    Данные изображения.

    id: уникальный идентификатор изображения
    source: объект ImageSource
    history: список применённых трансформаций
    created_at, updated_at: временные метки
    """

    source: ImageSource
    history: list[TransformationRecord]
    created_at: datetime
    updated_at: datetime | None
    id: str = field(default_factory=lambda: uuid4().hex)


@dataclass
class ImageFeatures:
    """
    Базовые признаки изображения.

    id: уникальный идентификатор записи
    image_id: ID изображения
    size: словарь {'width':..., 'height':...}
    format: формат изображения
    mean_brightness: средняя яркость
    contrast: стандартное отклонение яркости
    computed_at: время вычисления признаков
    """

    id: str
    image_id: str
    width: int
    height: int
    format: str
    mean_brightness: float
    contrast: float
    density: float
    histogram: list[int]
    computed_at: datetime = field(default_factory=datetime.utcnow)

from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

from src.entities import TransformationRecord, ImageSource


@dataclass
class ImageData:
    """
    Данные изображения.

    id: уникальный идентификатор изображения
    source: объект ImageSource
    original_format: исходный формат изображения
    width, height: размеры изображения
    current_state: путь к текущей версии изображения
    history: список применённых трансформаций
    created_at, updated_at: временные метки
    """
    id: str
    source: ImageSource
    original_format: str
    width: int
    height: int
    current_state: str
    history: List[TransformationRecord]
    created_at: datetime
    updated_at: datetime


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
    size: Dict[str, int]
    format: str
    mean_brightness: float
    contrast: float
    computed_at: datetime

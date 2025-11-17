from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

# ---------------------------
# Сущности проекта
# ---------------------------


@dataclass
class ImageSource:
    """
    Источник изображения.

    id: уникальный идентификатор источника
    source_type: тип источника ('file', 'url')
    location: путь к файлу или URL
    filename: имя файла
    created_at: время создания записи
    """
    id: str
    source_type: str
    location: str
    filename: str
    created_at: datetime


@dataclass
class TransformationRecord:
    """
    Запись о применённой трансформации.

    id: уникальный идентификатор трансформации
    image_id: ID изображения, к которому применена трансформация
    name: название трансформации ('resize', 'brightness', 'blur')
    params: параметры трансформации
    applied_at: время применения
    """
    id: str
    image_id: str
    name: str
    params: Dict
    applied_at: datetime


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


@dataclass
class JsonStorage:
    """
    Сохранение истории изменений в json.
    """


@dataclass
class Visualiser:
    """
    Визуализация.
    """
    id: str
    metrics_enabled: List[str]
    histogram_bins: int

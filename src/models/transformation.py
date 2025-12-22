from dataclasses import dataclass
from datetime import datetime

from ..core.processing import Options  # from src.core import Options


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
    name: Options
    params: dict
    applied_at: datetime

from dataclasses import dataclass
from typing import Dict
from datetime import datetime


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

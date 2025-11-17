from dataclasses import dataclass
from datetime import datetime


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

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class ImageSource:
    """
    Источник изображения.

    id: уникальный идентификатор источника
    location: путь к файлу или URL
    filename: имя файла
    created_at: время создания записи
    """

    id: str = field(default_factory=lambda: uuid4().hex)
    location: str = ''
    filename: str = ''
    created_at: datetime = field(default_factory=datetime.utcnow)

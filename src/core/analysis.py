from typing import List, Dict, Any, Optional
from PIL import Image


def apply_operation(img: Image.Image, op: Dict[str, Any]) -> Image.Image:
    """
    Применяет одну операцию (op: {'name':..., 'params':{...}}) и возвращает новое изображение.
    """
    pass


def analyze(
    path: str,
    operations: Optional[List[Dict[str, Any]]] = None,
    save_modified_to: Optional[str] = None,
) -> Dict[str, Any]:
    pass

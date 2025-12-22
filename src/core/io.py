import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from PIL import Image

from ..models import ImageData, ImageSource  # from src.models import ...
from .processing import Options

logger = logging.getLogger(__name__)


def ask_path() -> Path:
    """
    Принимает от пользователя путь к изображению.
    """
    while True:
        raw = input('Enter the path to the image: ').strip().strip('"').strip("'")
        path = Path(raw)
        if path.is_file():
            return path
        print(f'File not found: {path}. Try again.')


def ask_option() -> Options:
    """
    Принимает от пользователя режим трансформации.
    """
    available = [o.name for o in Options]  # Expected type 'collections. Iterable', got 'Type[Options]' instead
    prompt = (
        'Choose the transformstion regime:\n' + '\n'.join(f'  - {name}' for name in available) + '\nEnter the regime: '
    )
    while True:
        raw = input(prompt).strip()
        match = next((name for name in available if name.lower() == raw.lower()), None)
        if match is not None:
            return Options[match]  # Expected type 'Options', got 'Type[Options]' instead
        print('Wrong regime. Try again.')


def ask_int(prompt: str) -> int:
    """
    Принимает от пользователя целочисленные значения.
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if value <= 0:
                print('The value must be positive.')
                continue
            return value
        except ValueError:
            print('Enter an integer.')


def ask_params(option: Options) -> Any:
    """
    Принимает от пользователя параметры трансформации.
    """
    if option == Options.Resize:
        w = ask_int('Enter the width (px): ')
        h = ask_int('Enter the hight (px): ')
        return w, h

    if option == Options.Brightness:
        return input("Enter the Brightness value (for example, '1.2'): ").strip()

    if option == Options.Contrast:
        return input("Enter the Contrast value (for example, '1.1'): ").strip()

    if option == Options.Filter:
        return input("Enter the Filter (for example, 'blur', 'sharpen', 'edge_enhance', 'edges'): ").strip()

    return input('Enter the values ').strip()


def load_image(path: str) -> tuple[Image.Image, ImageSource, ImageData]:
    """
    Загружает изображение и возвращает (PIL.Image, ImageSource, ImageData).
    """
    logger.info('Loading image from %s', path)

    try:
        img = Image.open(path)
        logger.debug(
            'Image opened: size=%s, mode=%s, format=%s',
            getattr(img, 'size', None),
            getattr(img, 'mode', None),
            getattr(img, 'format', None),
        )

    except OSError:
        logger.exception('Failed to open image: %s', path)
        raise

    abs_path = os.path.abspath(path)
    source = ImageSource(
        location=abs_path,
        filename=os.path.basename(abs_path),
    )
    logger.debug('ImageSource created: %r', source)

    data = ImageData(
        source=source,
        history=[],
        created_at=datetime.utcnow(),
        updated_at=None,
    )
    logger.debug('ImageData created: %r', data)

    logger.info('Image loaded successfully from %s', path)
    return img, source, data


def save_image(img: Image.Image, path: str, formatting: str | None = None) -> None:
    """Сохраняет изображение по пути."""
    logger.info('Saving image to %s', path)

    if formatting is None:
        ext = os.path.splitext(path)[1].lower()
        if ext == '.jpg' or ext == '.jpeg':
            formatting = 'JPEG'
        elif ext == '.png':
            formatting = 'PNG'
        elif ext == '.webp':
            formatting = 'WEBP'
        else:
            formatting = img.format or 'PNG'
        logger.debug('Auto-detected image format for saving: %s (ext=%s)', formatting, ext)
    else:
        logger.debug('Using explicit image format for saving: %s', formatting)

    directory = os.path.dirname(path)
    if directory:
        try:
            os.makedirs(directory, exist_ok=True)
            logger.debug('Ensured directory exists: %s', directory)
        except OSError:
            logger.exception('Failed to create directory for path: %s', directory)
            raise

    try:
        img.save(path, format=formatting)
        logger.info('Image successfully saved to %s', path)

    except OSError:
        logger.exception('Failed to save image to %s with format %s', path, formatting)
        raise

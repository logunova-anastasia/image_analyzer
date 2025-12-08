from __future__ import annotations

import argparse
from pathlib import Path

from src.core.analysis import analyze, apply_operation
from src.core.io import load_image, save_image
from src.core.processing import Options
from src.core.visualization import compare_before_after, plot_histogram
from src.database.sqlite import init_db


def parse_args() -> argparse.Namespace:
    """
    Получает от пользователя аргументы: путь к изображению, опцию для трансформации и параметры.
    """
    parser = argparse.ArgumentParser(description='Простой CLI для анализа изображений и сохранения данных в SQLite')
    parser.add_argument(
        'image',
        type=Path,
        help='The path to the input image',
    )
    parser.add_argument(
        'option',
        type=str,
        choices=[o.name for o in Options],
        help='Ways to transform the image. Available options: Resize, Brightness, Contrast, Filter.',
    )

    parser.add_argument(
        'params',
        help='Parameters for transformations.',
    )

    return parser.parse_args()


def main() -> None:
    """
    Основная реализация.
    """
    args = parse_args()

    init_db()

    img_path: Path = args.image
    option: Options = Options[args.option]
    params = args.params

    if not img_path.is_file():
        raise SystemExit(f'Файл не найден: {img_path}')

    img, source, image_data = load_image(str(img_path))
    features = analyze(img, image_data.id)
    plot_histogram(features, 'data/plot.jpg')

    if option is not None:
        new_img, transformation = apply_operation(img, image_data, {option: params}, image_data.id)
        compare_before_after(img, new_img, 'data/comp.jpg')
        save_image(new_img, 'data/new.jpg')


if __name__ == '__main__':
    main()

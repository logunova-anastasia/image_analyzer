from __future__ import annotations

import logging
from pathlib import Path

from src.core.analysis import analyze, apply_operation
from src.core.io import ask_option, ask_params, ask_path, load_image, save_image
from src.core.visualization import compare_before_after, plot_histogram
from src.database import init_db

logger = logging.getLogger(__name__)


def main() -> None:
    logger.info('Starting image analysis CLI')

    logger.info('Initializing SQLite database')
    init_db()
    logger.info('Database initialized successfully')

    img_path = ask_path()
    option = ask_option()
    params = ask_params(option)
    new_name = input('Enter the name for the new file: ').strip()

    logger.info('Input image path: %s', img_path)
    logger.info('Selected option: %s', option.name)
    logger.info('Transformation params: %s', params)

    logger.info('Loading image')
    img, source, image_data = load_image(str(img_path))
    logger.debug('Image loaded. Source: %s, image_data: %r', source, image_data)

    logger.info('Analyzing image features')
    features = analyze(img, image_data.id)
    logger.debug('Extracted features: %r', features)

    plot_output_path = Path('data/plot.jpg')
    logger.info('Plotting histogram to %s', plot_output_path)
    plot_histogram(features, str(plot_output_path))

    logger.info('Applying transformation: %s', option.name)
    new_img, transformation = apply_operation(
        img,
        image_data,
        {option: params},
        image_data.id,
    )
    logger.debug('Applied transformation: %r', transformation)

    new_img_path = Path(f'data/{new_name}.jpg')
    logger.info('Saving before/after comparison')
    compare_before_after(img, new_img)

    logger.info('Saving transformed image to %s', new_img_path)
    save_image(new_img, str(new_img_path))

    logger.info('Processing finished successfully')
    print('All done!')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        filename='logging.log',
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    try:
        main()
    except Exception:
        logger.exception('Unhandled exception in CLI')
        raise

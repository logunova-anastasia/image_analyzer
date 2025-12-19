import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from PIL import Image

from ..models import ImageFeatures

logger = logging.getLogger(__name__)


def plot_histogram(result: ImageFeatures, save_path: str | None = None) -> None:
    """
    Рисует/сохраняет гистограмму на основе result['features']['histogram'].
    """
    logger.info('Plotting histogram for image %s', result.image_id)

    hist = result.histogram
    if hist is None:
        logger.error('Histogram is None for image %s', result.image_id)
        raise ValueError('Nothing to visualize.')

    hist_ar: NDArray[np.float32] = np.asarray(hist)
    if hist_ar.ndim != 1 or hist_ar.size == 0:
        logger.error('Invalid histogram for image %s: shape=%s', result.image_id, hist_ar.shape)
        raise ValueError('Nothing to visualize.')

    logger.debug(
        'Histogram array shape: %s, min=%s, max=%s',
        hist_ar.shape,
        float(np.min(hist_ar)),
        float(np.max(hist_ar)),
    )

    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.style'] = 'normal'
    fig, ax = plt.subplots(figsize=(8, 4))

    x = np.arange(hist_ar.size)
    ax.bar(x, hist_ar, width=1.0)

    ax.set_title('Histogram')
    ax.set_xlabel('Brightness')
    ax.set_ylabel('The number of pixels')
    ax.set_xlim(0, hist_ar.size - 1)

    plt.tight_layout()

    try:
        if save_path is not None:
            saved_path = Path(save_path)
            logger.info('Saving histogram to %s', saved_path)
            saved_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(saved_path, bbox_inches='tight', dpi=200, facecolor='white')
        else:
            logger.debug('Showing histogram interactively')
            plt.show()
    finally:
        plt.close(fig)


def compare_before_after(original: Image.Image, modified: Image.Image) -> None:
    """
    Создаёт коллаж 'до/после' и сохраняет/показывает.
    """
    logger.info(
        "Creating 'before/after' comparison: original_size=%s, modified_size=%s",
        getattr(original, 'size', None),
        getattr(modified, 'size', None),
    )

    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.style'] = 'normal'
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    ax1.imshow(original.convert('RGB'))
    ax1.set_title('Original')
    ax1.axis('off')

    ax2.imshow(modified.convert('RGB'))
    ax2.set_title('Modified')
    ax2.axis('off')

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.02, hspace=0.02)

    try:
        saved_path = Path('data/comparison.jpg')
        logger.info("Saving 'before/after' comparison to %s", saved_path)
        saved_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(saved_path, bbox_inches='tight', dpi=200, facecolor='white')

    finally:
        plt.close(fig)

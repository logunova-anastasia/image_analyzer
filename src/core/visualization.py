from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from ..models.image import ImageFeatures


def plot_histogram(result: ImageFeatures, save_path: str | None = None) -> None:
    """
    Рисует/сохраняет гистограмму на основе result['features']['histogram'].
    """
    hist = result.histogram
    if hist is None:
        raise ValueError('Nothing to visualize.')

    hist_ar = np.asarray(hist)

    fig, ax = plt.subplots(figsize=(8, 4))

    x = np.arange(len(hist_ar))
    ax.bar(x, hist_ar)

    ax.set_title('Histogram')
    ax.set_xlabel('Brightness')
    ax.set_ylabel('The number of pixels')
    ax.set_xlim(0, len(hist_ar) - 1)

    plt.tight_layout()

    if save_path is not None:
        saved_path = Path(save_path)
        saved_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(saved_path)
        plt.close(fig)
    else:
        plt.show()


def compare_before_after(original: Image.Image, modified: Image.Image, save_path: str | None = None) -> None:
    """
    Создаёт коллаж 'до/после' и сохраняет/показывает.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    ax1.imshow(original.convert('RGB'))
    ax1.set_title('Original')
    ax1.axis('off')

    ax2.imshow(modified.convert('RGB'))
    ax2.set_title('Modified')
    ax2.axis('off')

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.02, hspace=0.02)

    if save_path is not None:
        saved_path = Path(save_path)
        saved_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(saved_path, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()

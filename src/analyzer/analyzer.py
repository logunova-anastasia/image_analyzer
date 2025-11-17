from dataclasses import dataclass
from typing import List


@dataclass
class Visualiser:
    """
    Визуализация.
    """
    id: str
    metrics_enabled: List[str]
    calc_histogram: bool = True
    histogram_bins: int = 256

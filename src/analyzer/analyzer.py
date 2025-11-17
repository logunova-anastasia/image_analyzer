from dataclasses import dataclass
from typing import List


@dataclass
class Visualiser:
    """
    Визуализация.
    """
    id: str
    metrics_enabled: List[str]
    histogram_bins: int

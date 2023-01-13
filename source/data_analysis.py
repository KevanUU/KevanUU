from typing import TYPE_CHECKING

import pandas as pd

from utils.io import read_csv, save_csv

if TYPE_CHECKING:
    from utils.config import Config


class DataAnalyzer:

    def __init__(self, cfg: "Config"):
        self.cfg = cfg

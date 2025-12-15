import pandas as pd
from dataclasses import dataclass

from stages.base import Stage


@dataclass
class Pipeline:
    """Class for processing pipeline stages."""

    stages: list[Stage]

    def run(self, dataframes: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        for stage in self.stages:
            dataframes = stage.process(dataframes)
        return dataframes

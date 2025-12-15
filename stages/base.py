import pandas as pd
from abc import ABC, abstractmethod


class Stage(ABC):
    """
    The abstract base class for all stages.
    Pass dataframe and return processed dataframe.
    """

    @staticmethod
    @abstractmethod
    def process(dataframes: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        pass

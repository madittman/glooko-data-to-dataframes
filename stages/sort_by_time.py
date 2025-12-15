import pandas as pd

from stages.base import Stage


class SortByTime(Stage):
    """Sort all dataframes by time column."""

    @staticmethod
    def process(dataframes: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        for dataframe_name in dataframes.keys():
            dataframes[dataframe_name] = dataframes[dataframe_name].sort_values(
                by=["time"]
            )

        return dataframes

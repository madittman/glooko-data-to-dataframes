import pandas as pd

from stages.base import Stage


class Merge(Stage):
    """
    Merge all dataframe into one.
    This stage should come after RenameColumns.
    """

    @staticmethod
    def process(dataframes: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        # Merge all dataframes
        all_columns: pd.DataFrame = pd.concat(
            list(dataframes.values()), ignore_index=True
        )

        # Keep merged dataframe as new key
        dataframes = {"all_columns": all_columns}

        return dataframes

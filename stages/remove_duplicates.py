import pandas as pd

from stages.base import Stage


class RemoveDuplicates(Stage):
    """
    Remove or merge all duplicate rows.
    This stage should come after SplitIntoNormalizedTables.
    """

    @staticmethod
    def process(dataframes: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        glucose_values: pd.DataFrame = dataframes["glucose_values"]
        basal: pd.DataFrame = dataframes["basal"]
        bolus: pd.DataFrame = dataframes["bolus"]

        # Merge duplicates by summing up other columns
        basal = basal.groupby("time", as_index=False).sum()
        bolus = bolus.groupby("time", as_index=False).sum()

        # Drop rows where all insulin units are 0
        bolus = bolus.drop(
            bolus[
                (bolus["insulin_delivered_in_u"] == 0)
                & (bolus["initial_delivery_in_u"] == 0)
                & (bolus["extended_delivery_in_u"] == 0)
            ].index
        )

        # Update dataframes
        dataframes = {
            "glucose_values": glucose_values,
            "basal": basal,
            "bolus": bolus,
        }

        return dataframes

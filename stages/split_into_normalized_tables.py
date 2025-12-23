import numpy as np
import pandas as pd

from stages.base import Stage


class SplitIntoNormalizedTables(Stage):
    """
    Split dataframe into normalized tables.
    This stage should come after Clean.
    """

    @staticmethod
    def process(dataframes: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        all_columns: pd.DataFrame = dataframes["all_columns"]

        gluco_vals: pd.DataFrame = all_columns[["time", "glucose_value_in_mg/dl"]]
        basal: pd.DataFrame = all_columns[["time", "duration_in_min", "basal_rate"]]
        bolus: pd.DataFrame = all_columns[
            [
                "time",
                "carbs_input_in_g",
                "insulin_delivered_in_u",
                "initial_delivery_in_u",
                "extended_delivery_in_u",
            ]
        ]

        # Drop rows with no information
        gluco_vals = gluco_vals.dropna(
            how="all", subset=[col for col in gluco_vals.columns if col != "time"]
        )
        basal = basal.dropna(
            how="all", subset=[col for col in basal.columns if col != "time"]
        )
        bolus = bolus.dropna(
            how="all", subset=[col for col in bolus.columns if col != "time"]
        )

        # Convert initial and extended insulin units with NaN to 0
        bolus["initial_delivery_in_u"] = bolus["initial_delivery_in_u"].replace(
            np.nan, 0
        )
        bolus["extended_delivery_in_u"] = bolus["extended_delivery_in_u"].replace(
            np.nan, 0
        )

        # Update dataframes
        dataframes = {
            "glucose_values": gluco_vals,
            "basal": basal,
            "bolus": bolus,
        }
        return dataframes

import numpy as np
import pandas as pd

from stages.base import Stage


class Clean(Stage):
    """
    Clean the dataframe columns.
    This stage should come after Merge.
    """

    @staticmethod
    def process(dataframes: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        all_columns: pd.DataFrame = dataframes["all_columns"].copy()

        # Drop row if every single value is NaN (this shouldn't be the case)
        all_columns = all_columns.dropna(axis=1, how="all")

        # Drop redundant columns
        all_columns = all_columns.drop(
            columns=[
                "manual_reading",
                "serial_number",
                "bolus_insulin_type",
                "carbs_ratio",
                "basal_insulin_type",
            ]
        )

        # Clip maximum glucose value to 400 (as the tslim cannot measure those values)
        all_columns["glucose_value_in_mg/dl"] = all_columns[
            "glucose_value_in_mg/dl"
        ].clip(upper=400)

        # Convert all glucose values with 0 to NaN
        all_columns["glucose_value_in_mg/dl"] = all_columns[
            "glucose_value_in_mg/dl"
        ].replace(0, np.nan)

        # Convert glucose value to int
        all_columns["glucose_value_in_mg/dl"] = all_columns[
            "glucose_value_in_mg/dl"
        ].astype("Int64")

        # Round insulin rates (as the tslim only measures with two decimal places)
        all_columns["insulin_delivered_in_u"] = all_columns[
            "insulin_delivered_in_u"
        ].round(2)
        all_columns["initial_delivery_in_u"] = all_columns[
            "initial_delivery_in_u"
        ].round(2)
        all_columns["extended_delivery_in_u"] = all_columns[
            "extended_delivery_in_u"
        ].round(2)
        all_columns["basal_rate"] = all_columns["basal_rate"].round(2)

        # Update dataframe
        dataframes = {
            "all_columns": all_columns,
        }
        return dataframes

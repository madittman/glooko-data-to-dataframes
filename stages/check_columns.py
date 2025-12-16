import pandas as pd

from exceptions import ColumnsChangedError
from stages.base import Stage


# Global variable to check columns on
expected_columns_by_dataframe: dict[str, list[str]] = {
    "bg_data_1": [
        "Timestamp",
        "Glucose Value (mg/dl)",
        "Manual Reading",
        "Serial Number",
    ],
    "cgm_data_1": [
        "Timestamp",
        "CGM Glucose Value (mg/dl)",
        "Serial Number",
    ],
    "cgm_data_2": [
        "Timestamp",
        "CGM Glucose Value (mg/dl)",
        "Serial Number",
    ],
    "basal_data_1": [
        "Timestamp",
        "Insulin Type",
        "Duration (minutes)",
        "Percentage (%)",
        "Rate",
        "Insulin Delivered (U)",
        "Serial Number",
    ],
    "bolus_data_1": [
        "Timestamp",
        "Insulin Type",
        "Blood Glucose Input (mg/dl)",
        "Carbs Input (g)",
        "Carbs Ratio",
        "Insulin Delivered (U)",
        "Initial Delivery (U)",
        "Extended Delivery (U)",
        "Serial Number",
    ],
}


class CheckColumns(Stage):
    """
    Check no columns have changed.
    This should be the first stage.
    """

    @staticmethod
    def process(dataframes: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        # Raise error if the columns of a file have changed

        if set(dataframes["bg_data_1"].columns.tolist()) != set(
            expected_columns_by_dataframe["bg_data_1"]
        ):
            raise ColumnsChangedError("Columns have changed in bg_data_1")

        if set(dataframes["cgm_data_1"].columns.tolist()) != set(
            expected_columns_by_dataframe["cgm_data_1"]
        ):
            raise ColumnsChangedError("Columns have changed in cgm_data_1")

        # Only read in 'cgm_data_2.csv' if it is there
        if dataframes["cgm_data_2"].empty:
            dataframes.pop("cgm_data_2")
        else:
            if set(dataframes["cgm_data_2"].columns.tolist()) != set(
                expected_columns_by_dataframe["cgm_data_2"]
            ):
                raise ColumnsChangedError("Columns have changed in cgm_data_2")

        if set(dataframes["basal_data_1"].columns.tolist()) != set(
            expected_columns_by_dataframe["basal_data_1"]
        ):
            raise ColumnsChangedError("Columns have changed in basal_data_1")

        if set(dataframes["bolus_data_1"].columns.tolist()) != set(
            expected_columns_by_dataframe["bolus_data_1"]
        ):
            raise ColumnsChangedError("Columns have changed in bolus_data_1")

        return dataframes

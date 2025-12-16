import pandas as pd

from stages.base import Stage


class RenameColumns(Stage):
    """
    Rename columns as snake case.
    This stage should come after CheckColumns.
    """

    @staticmethod
    def process(dataframes: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        glucose_values_1: pd.DataFrame = dataframes["bg_data_1"]
        glucose_values_2: pd.DataFrame = dataframes["cgm_data_1"]
        glucose_values_3: pd.DataFrame = dataframes["cgm_data_2"]
        basal: pd.DataFrame = dataframes["basal_data_1"]
        bolus: pd.DataFrame = dataframes["bolus_data_1"]

        glucose_values_1 = glucose_values_1.rename(
            columns={
                "Timestamp": "time",
                "Glucose Value (mg/dl)": "glucose_value_in_mg/dl",
                "Manual Reading": "manual_reading",
                "Serial Number": "serial_number",
            }
        )
        glucose_values_2 = glucose_values_2.rename(
            columns={
                "Timestamp": "time",
                "CGM Glucose Value (mg/dl)": "glucose_value_in_mg/dl",
                "Serial Number": "serial_number",
            }
        )
        glucose_values_3 = glucose_values_3.rename(
            columns={
                "Timestamp": "time",
                "CGM Glucose Value (mg/dl)": "glucose_value_in_mg/dl",
                "Serial Number": "serial_number",
            }
        )
        basal = basal.rename(
            columns={
                "Timestamp": "time",
                "Insulin Type": "basal_insulin_type",
                "Duration (minutes)": "duration_in_min",
                "Percentage (%)": "percentage",
                "Rate": "basal_rate",
                "Insulin Delivered (U)": "insulin_delivered_in_u",
                "Serial Number": "serial_number",
            }
        )
        bolus = bolus.rename(
            columns={
                "Timestamp": "time",
                "Insulin Type": "bolus_insulin_type",
                "Blood Glucose Input (mg/dl)": "glucose_value_in_mg/dl",
                "Carbs Input (g)": "carbs_input_in_g",
                "Carbs Ratio": "carbs_ratio",
                "Insulin Delivered (U)": "insulin_delivered_in_u",
                "Initial Delivery (U)": "initial_delivery_in_u",
                "Extended Delivery (U)": "extended_delivery_in_u",
                "Serial Number": "serial_number",
            }
        )

        # Update dataframes
        dataframes = {
            "glucose_values_1": glucose_values_1,
            "glucose_values_2": glucose_values_2,
            "glucose_values_3": glucose_values_3,
            "bolus": bolus,
            "basal": basal,
        }
        return dataframes

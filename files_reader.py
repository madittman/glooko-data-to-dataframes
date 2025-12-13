from typing import Dict, List
from pathlib import Path
import pandas as pd
import os

from exceptions import ColumnsChangedError, FilenamesChangedError


class FilesReader:
    """
    Class for reading in CSV files and checking no filenames and columns have changed.
    """

    expected_columns_by_file: Dict[str, List[str]] = {
        "bg_data_1.csv": [
            "Timestamp",
            "Glucose Value (mg/dl)",
            "Manual Reading",
            "Serial Number",
        ],
        "cgm_data_1.csv": [
            "Timestamp",
            "CGM Glucose Value (mg/dl)",
            "Serial Number",
        ],
        "cgm_data_2.csv": [
            "Timestamp",
            "CGM Glucose Value (mg/dl)",
            "Serial Number",
        ],
        "Insulin data/basal_data_1.csv": [
            "Timestamp",
            "Insulin Type",
            "Duration (minutes)",
            "Percentage (%)",
            "Rate",
            "Insulin Delivered (U)",
            "Serial Number",
        ],
        "Insulin data/bolus_data_1.csv": [
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
    bg_data_1: pd.DataFrame = pd.DataFrame()
    cgm_data_1: pd.DataFrame = pd.DataFrame()
    cgm_data_2: pd.DataFrame = pd.DataFrame()
    basal_data_1: pd.DataFrame = pd.DataFrame()
    bolus_data_1: pd.DataFrame = pd.DataFrame()

    def __init__(self, root_dir: str):
        self.root_dir: Path = Path(root_dir)

        # Raise error if filenames have changed
        if not self.check_filenames():
            raise FilenamesChangedError("Filenames have changed")

        # Set dataframes
        self.read_in_files()

        # Raise error if columns in a file have changed
        if not self.check_columns(
            actual_columns=self.bg_data_1.columns.tolist(),
            expected_columns=self.expected_columns_by_file["bg_data_1.csv"],
        ):
            raise ColumnsChangedError(f"Columns have changed in bg_data_1.csv")

        if not self.check_columns(
            actual_columns=self.cgm_data_1.columns.tolist(),
            expected_columns=self.expected_columns_by_file["cgm_data_1.csv"],
        ):
            raise ColumnsChangedError(f"Columns have changed in cgm_data_1.csv")

        if not self.check_columns(
            actual_columns=self.cgm_data_2.columns.tolist(),
            expected_columns=self.expected_columns_by_file["cgm_data_2.csv"],
        ):
            raise ColumnsChangedError(f"Columns have changed in cgm_data_2.csv")

        if not self.check_columns(
            actual_columns=self.basal_data_1.columns.tolist(),
            expected_columns=self.expected_columns_by_file[
                "Insulin data/basal_data_1.csv"
            ],
        ):
            raise ColumnsChangedError(
                f"Columns have changed in Insulin data/basal_data_1.csv"
            )

        if not self.check_columns(
            actual_columns=self.bolus_data_1.columns.tolist(),
            expected_columns=self.expected_columns_by_file[
                "Insulin data/bolus_data_1.csv"
            ],
        ):
            raise ColumnsChangedError(
                f"Columns have changed in Insulin data/bolus_data_1.csv"
            )

    def check_filenames(self) -> bool:
        """Return False if filenames have changed."""
        actual_filenames: List[str] = []
        for filename in self.root_dir.rglob("*"):
            if filename.is_file():
                filename = filename.relative_to(
                    self.root_dir
                )  # Strip off the root_dir prefix
                actual_filenames.append(str(filename))
        expected_filenames: List[str] = list(self.expected_columns_by_file.keys())
        return set(actual_filenames) == set(expected_filenames)

    def read_in_files(self) -> None:
        """Read in CSV files and set to DataFrames."""
        self.bg_data_1: pd.DataFrame = pd.read_csv(
            os.path.join(str(self.root_dir), "bg_data_1.csv"),
            skiprows=1,
        )
        self.cgm_data_1: pd.DataFrame = pd.read_csv(
            os.path.join(str(self.root_dir), "cgm_data_1.csv"),
            skiprows=1,
        )
        self.cgm_data_2: pd.DataFrame = pd.read_csv(
            os.path.join(str(self.root_dir), "cgm_data_2.csv"),
            skiprows=1,
        )
        self.basal_data_1: pd.DataFrame = pd.read_csv(
            os.path.join(str(self.root_dir), "Insulin data/basal_data_1.csv"),
            skiprows=1,
        )
        self.bolus_data_1: pd.DataFrame = pd.read_csv(
            os.path.join(str(self.root_dir), "Insulin data/bolus_data_1.csv"),
            skiprows=1,
        )

    @staticmethod
    def check_columns(actual_columns: List[str], expected_columns: List[str]) -> bool:
        """Return False if columns have changed."""
        return set(actual_columns) == set(expected_columns)

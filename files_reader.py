import os
import pandas as pd
import re
from pathlib import Path

from exceptions import FilenamesChangedError


# These files need to be there
basic_filenames: list[str] = [
    "bg_data_1.csv",
    "cgm_data_1.csv",
    "basal_data_1.csv",
    "bolus_data_1.csv",
]


class FilesReader:
    """
    Class for reading in CSV files and checking no filenames and have changed.
    """

    dataframes: dict[str, pd.DataFrame] = {
        "bg_data_1": pd.DataFrame(),
        "cgm_data_1": pd.DataFrame(),
        "basal_data_1": pd.DataFrame(),
        "bolus_data_1": pd.DataFrame(),
    }

    def __init__(self, root_dir: str):
        self.root_dir: Path = Path(root_dir)

        # Raise error if filenames have changed
        if not set(basic_filenames) <= set(self.get_actual_filenames()):
            raise FilenamesChangedError("Filenames have changed")

        # Set dataframes
        self.read_in_files()

    def get_actual_filenames(self) -> list[str]:
        """Return list of actual filenames."""
        actual_filenames: list[str] = []
        for filepath in self.root_dir.rglob("*"):
            if filepath.is_file():
                # Only keep filename
                parts: list[str] = re.split(r"[/\\]", str(filepath))
                actual_filename: str = parts[-1]
                actual_filenames.append(actual_filename)
        return actual_filenames

    def read_in_files(self) -> None:
        """Read in CSV files and set dataframes."""
        self.dataframes["bg_data_1"] = pd.read_csv(
            os.path.join(str(self.root_dir), "bg_data_1.csv"),
            skiprows=1,
        )
        self.dataframes["cgm_data_1"] = pd.read_csv(
            os.path.join(str(self.root_dir), "cgm_data_1.csv"),
            skiprows=1,
        )

        # Only read in 'cgm_data_2.csv' if it is there
        self.dataframes["cgm_data_2"] = pd.DataFrame()
        if os.path.exists("cgm_data_2.csv"):
            self.dataframes["cgm_data_2"] = pd.read_csv(
                os.path.join(str(self.root_dir), "cgm_data_2.csv"),
                skiprows=1,
            )

        self.dataframes["basal_data_1"] = pd.read_csv(
            os.path.join(str(self.root_dir), "Insulin data/basal_data_1.csv"),
            skiprows=1,
        )
        self.dataframes["bolus_data_1"] = pd.read_csv(
            os.path.join(str(self.root_dir), "Insulin data/bolus_data_1.csv"),
            skiprows=1,
        )

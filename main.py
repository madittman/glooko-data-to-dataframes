import os
import pandas as pd

from files_reader import FilesReader
from pipeline import Pipeline
from stages.check_columns import CheckColumns
from stages.clean import Clean
from stages.merge import Merge
from stages.remove_duplicates import RemoveDuplicates
from stages.rename_columns import RenameColumns
from stages.sort_by_time import SortByTime
from stages.split_into_normalized_tables import SplitIntoNormalizedTables


def main() -> None:
    # Read CSV files
    files_reader: FilesReader = FilesReader(
        root_dir="Insert root directory here...",
    )
    raw_dataframes: dict[str, pd.DataFrame] = files_reader.dataframes

    pipeline: Pipeline = Pipeline(
        stages=[
            CheckColumns(),
            RenameColumns(),
            Merge(),
            Clean(),
            SplitIntoNormalizedTables(),
            RemoveDuplicates(),
            SortByTime(),
        ],
    )
    processed_dataframes: dict[str, pd.DataFrame] = pipeline.run(raw_dataframes)

    # --- TESTING ---
    # Create CSVs from dataframes
    output_dir: str = "Insert output directory here..."
    for key in processed_dataframes.keys():
        processed_dataframes[key].to_csv(
            os.path.join(output_dir, key + ".csv"), index=False
        )
    # Get all duplicated timestamps
    for key in processed_dataframes.keys():
        dupes: pd.DataFrame = processed_dataframes[key][
            processed_dataframes[key]["time"].duplicated(keep=False)
        ]
        dupes.to_csv(os.path.join(output_dir, key + "_dupes.csv"), index=False)


if __name__ == "__main__":
    main()

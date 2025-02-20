from typing import override

import pandas as pd

from frameworks.framework import Framework
from models.guideline import Guideline

FEW_SHOTS = {}

DATA_FILE_PATH = "data/owasp-scvs/OWASP_SCVS-1.0.csv"
FEW_SHOTS_FILE_PATH = "data/owasp-scvs/few_shots.json"
SYSTEM_PROMPTS = [
    """
You are a guideline decomposition assistant. Your task is to take a given guideline that may contain compound statements or multiple components and break it down into smaller, independent guidelines. Keep all original meanings and intents intact. The decomposed guidelines should be independent and self-contained. Only include information that is explicitly stated in the original text.

Let's think step by step...
    """
]


class SCVS(Framework):
    def __init__(self) -> None:
        self._few_shot_file_path: str = FEW_SHOTS_FILE_PATH
        try:
            self._csv: pd.DataFrame = pd.read_csv(DATA_FILE_PATH)
        except FileNotFoundError as e:
            raise RuntimeError(f"CSV file not found at {DATA_FILE_PATH}") from e
        except pd.errors.ParserError as e:
            raise RuntimeError("Error parsing CSV file") from e
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while reading the CSV: {e}"
            ) from e

        super().__init__()

    @override
    def guidelines(self) -> list[Guideline]:
        guidelines: list[Guideline] = []
        for index, row in self._csv.iterrows():
            try:
                # Get values with default None if not found.
                raw_id = row.get("id")
                raw_text = row.get("text")

                if raw_id is None or pd.isna(raw_id):
                    raise ValueError(f"Missing or invalid 'id' in row {index}")
                if raw_text is None or pd.isna(raw_text):
                    raise ValueError(f"Missing or invalid 'text' in row {index}")

                # Ensure values are strings.
                guideline_id: str = str(raw_id)
                guideline_short: str = str(raw_text)

                # determine level
                level = None
                if row.get("l1") is True:
                    level = "L1"
                elif row.get("l2") is True:
                    level = "L2"
                elif row.get("l3") is True:
                    level = "L3"

                guideline = Guideline(
                    id=guideline_id,
                    short=guideline_short,
                    long=None,
                    context=None,
                    level=level,
                )
                guidelines.append(guideline)
            except Exception as row_error:
                print(f"Error processing row {index}: {row_error}")
                continue

        return guidelines

    @property
    @override
    def name(self) -> str:
        return "owasp-scvs"

    @property
    @override
    def system_prompt(self) -> list[str]:
        return SYSTEM_PROMPTS

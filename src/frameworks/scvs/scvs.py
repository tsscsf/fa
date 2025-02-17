import json
from typing import override

import pandas as pd

from frameworks.framework import Framework
from models.few_shot import FewShotExample
from models.guideline import Guideline

FEW_SHOTS = {}


class SCVS(Framework):
    def __init__(self) -> None:
        try:
            self._csv: pd.DataFrame = pd.read_csv("data/OWASP_SCVS-1.0.csv")
        except FileNotFoundError as e:
            raise RuntimeError("CSV file not found at 'data/OWASP_SCVS-1.0.csv'") from e
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

    @override
    def few_shots(self) -> list[FewShotExample]:
        examples: list[FewShotExample] = []
        with open("data/few_shots.json") as f:
            few_shots_data = json.load(f)  # pyright: ignore[reportAny]

        for i in few_shots_data:  # pyright: ignore[reportAny]
            model = FewShotExample.model_validate(i)
            examples.append(model)

        return examples

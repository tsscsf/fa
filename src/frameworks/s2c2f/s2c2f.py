from typing import override

from frameworks.framework import Framework
from models.guideline import Guideline

FEW_SHOTS_FILE_PATH = "data/microsoft-s2c2f/few_shots.json"


class S2C2F(Framework):
    def __init__(self) -> None:
        self._few_shot_file_path: str = FEW_SHOTS_FILE_PATH
        super().__init__()

    def _md_to_guidelines(self, table_str: str) -> list[Guideline]:
        # Split the string into lines and remove any completely empty lines
        lines: list[str] = [
            line for line in table_str.strip().splitlines() if line.strip()
        ]

        # The first line is the header row.
        header_line: str = lines[0]

        # The second line is the separator row (e.g., | --- | --- | ...),
        # so the data lines start from index 2.
        data_lines: list[str] = lines[2:]

        # Extract header cells by splitting on '|' and ignoring the first and last empty items
        header_cells: list[str] = header_line.split("|")[1:-1]
        # Remove Markdown formatting (like '**' or '*') from the header cells
        headers: list[str] = [h.strip().strip("*").strip() for h in header_cells]

        guidelines: list[Guideline] = []
        current_practice: str | None = None

        for line in data_lines:
            # Split on '|' and ignore the first and last empty strings
            row_cells: list[str] = line.split("|")[1:-1]
            # Strip whitespace from each cell
            row_cells = [cell.strip() for cell in row_cells]

            # If the Practice cell is empty, inherit the previous one.
            if not row_cells[0]:
                if current_practice is not None:
                    row_cells[0] = current_practice
                else:
                    row_cells[0] = ""
            else:
                current_practice = row_cells[0]

            # Zip the headers and row cells into a dictionary
            row_dict: dict[str, str] = dict(zip(headers, row_cells, strict=False))
            guideline = Guideline(
                id=row_dict["Requirement ID"],
                short=row_dict["Requirement Title"],
                long=None,
                context=None,
                level=row_dict["Maturity Level"],
            )
            guidelines.append(guideline)

        return guidelines

    @override
    def guidelines(self) -> list[Guideline]:
        with open(
            "data/microsoft-s2c2f/guidelines.md",
        ) as f:
            filecontent = f.read()
            guidelines = self._md_to_guidelines(filecontent)
        return guidelines

    @property
    @override
    def name(self) -> str:
        return "microsoft-s2c2f"

import json
from typing import override

from frameworks.framework import Framework
from models.guideline import Guideline

FEW_SHOTS_FILE_PATH = "data/sok/few_shots.json"
SAFEGUARDS_FILE_PATH = "data/sok/safeguards.json"
type SafeguardsData = list[dict[str, str | list[dict[str, str | bool]]]]


class SoK(Framework):
    def __init__(self) -> None:
        self._few_shot_file_path: str = FEW_SHOTS_FILE_PATH
        with open(SAFEGUARDS_FILE_PATH) as f:
            data: SafeguardsData = json.load(f)
            self._guidelines: list[Guideline] = self._load_guidelines(data)
        super().__init__()

    def _load_guidelines(self, fc: SafeguardsData) -> list[Guideline]:
        guidelines: list[Guideline] = []
        for sg in fc:
            info_list = sg.get("info", [])
            if not info_list or not isinstance(info_list, list):
                continue  # or handle the missing info case appropriately

            info = info_list[0]

            description = info.get("Description")
            desc = f"{description}\n\n" if description else ""

            # Append key-value pairs if they exist and are non-empty.
            for key in ["Project Maintainer", "Administrator", "Downstream User"]:
                value = info.get(key)
                if value:  # Only include if value is truthy (non-empty)
                    desc += f"{key}: {value}\n"

            guideline = Guideline(
                id=str(sg.get("sgId", "")),
                short=str(sg.get("sgName", "")),
                long=desc,
                context=None,
                level=None,
            )
            guidelines.append(guideline)

        return guidelines

    @override
    def guidelines(self) -> list[Guideline]:
        return self._guidelines

    @property
    @override
    def name(self) -> str:
        return "sok"

import json
from typing import override

from frameworks.framework import Framework
from models.guideline import Guideline

FEW_SHOTS_FILE_PATH = "data/microsoft-s2c2f/few_shots.json"
SAFEGUARDS_FILE_PATH = "data/sok/safeguards.json"
type SafeguardsData = list[dict[str, str | list[dict[str, str | bool]]]]


class SoK(Framework):
    def __init__(self) -> None:
        super().__init__()
        with open(SAFEGUARDS_FILE_PATH) as f:
            data: SafeguardsData = json.load(f)
            self._guidelines: list[Guideline] = self._load_guidelines(data)

    def _load_guidelines(self, fc: SafeguardsData) -> list[Guideline]:
        guidelines: list[Guideline] = []
        for sg in fc:
            desc = str(sg["Description"]) + "\n\n"
            for key in ["Project Maintainer", "Administrator", "Downstream User"]:
                desc += f"{key}: {sg[key]}\n"

            guideline = Guideline(
                id=str(sg["sgId"]),
                short=str(sg["sgName"]),
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

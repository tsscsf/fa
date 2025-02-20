import json
from typing import override

from frameworks.framework import Framework
from models.guideline import Guideline

FEW_SHOTS_FILE_PATH = "data/sok/few_shots.json"
SAFEGUARDS_FILE_PATH = "data/sok/safeguards.json"
SYSTEM_PROMPT_1 = """
You are an actionable guideline decomposition assistant. The decomposed guidelines should be independent and self-contained. Only include information that can be applied, do not include facts or definitions. Your task is to take a given guideline that may contain compound statements or multiple components and break it down into smaller, independent guidelines if possible. Keep all original meanings and intents intact. Do not infer information that is not explicitly stated in the original text.

Let's think step by step...
"""

SYSTEM_PROMPT_2 = """
You are a guideline decomposition assistant. You are given a list of guidelines that may contain compound statements or multiple components. Your task is to break down the guidelines into smaller, independent guidelines if possible while keeping all original meanings and intents intact. The decomposed guidelines should be independent and self-contained. Do not infer information that is not explicitly stated in the original text.

Let's think step by step...
"""
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

    @property
    @override
    def system_prompt(self) -> list[str]:
        return [SYSTEM_PROMPT_1, SYSTEM_PROMPT_2]

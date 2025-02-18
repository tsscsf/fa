import json
from abc import ABC, abstractmethod

from models.few_shot import FewShotExample
from models.guideline import Guideline


class Framework(ABC):
    def __init__(self) -> None:
        self._few_shot_file_path: str

        super().__init__()

    @abstractmethod
    def guidelines(self) -> list[Guideline]:
        pass

    def few_shots(self) -> list[FewShotExample]:
        if not self._few_shot_file_path:
            raise RuntimeError(f"Few shot file path not set for {self.name}")

        examples: list[FewShotExample] = []
        with open(self._few_shot_file_path) as f:
            few_shots_data = json.load(f)  # pyright: ignore[reportAny]

        for i in few_shots_data:  # pyright: ignore[reportAny]
            model = FewShotExample.model_validate(i)
            examples.append(model)

        return examples

    @property
    @abstractmethod
    def name(self) -> str:
        pass

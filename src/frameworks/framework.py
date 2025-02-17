from abc import ABC, abstractmethod

from models.few_shot import FewShotExample
from models.guideline import Guideline


class Framework(ABC):
    @abstractmethod
    def guidelines(self) -> list[Guideline]:
        pass

    @abstractmethod
    def few_shots(self) -> list[FewShotExample]:
        pass

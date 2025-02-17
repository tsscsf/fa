from abc import ABC, abstractmethod

from models.guideline import Guideline


class Framework(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def guidelines(self) -> list[Guideline]:
        pass

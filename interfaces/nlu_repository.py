# interfaces/nlu_repository.py
from abc import ABC, abstractmethod

class NLURepository(ABC):
    @abstractmethod
    def process_message(self, text: str, language: str):
        pass
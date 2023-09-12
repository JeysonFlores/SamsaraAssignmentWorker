from abc import ABC, abstractmethod


class BaseExporter(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def export(self, data):
        raise Exception("Method export isn't implemented")

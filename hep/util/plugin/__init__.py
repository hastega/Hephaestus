from abc import ABC, abstractmethod
from argparse import ArgumentParser


class HepPlugin(ABC):
    @abstractmethod
    def name(self, hep_parser: ArgumentParser) -> str:
        pass

    @abstractmethod
    def version(self, hep_parser: ArgumentParser) -> str:
        pass

    @abstractmethod
    def authors(self, hep_parser: ArgumentParser) -> list[str]:
        pass

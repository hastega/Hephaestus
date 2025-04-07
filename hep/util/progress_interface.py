from abc import ABC, abstractmethod
from enum import Enum

from git import RemoteProgress


class ProgressInterface(RemoteProgress, ABC):
    @abstractmethod
    def __init__(self):
        super().__init__()

    @abstractmethod
    def setup(self, name: str, status: Enum):
        pass

    @abstractmethod
    def update(self, op_code, cur_count, max_count=None, message=""):
        pass

    @abstractmethod
    def close(self) -> None:
        pass

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from system import System


class App(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def init(self, system: "System") -> None:
        pass

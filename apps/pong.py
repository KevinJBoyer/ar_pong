from typing import TYPE_CHECKING
from apps.app import App

if TYPE_CHECKING:
    from system import System


class Pong(App):
    def __init__(self):
        self.name = "Pong"

    def init(self, system: "System") -> None:
        pass

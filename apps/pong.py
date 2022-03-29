import pyglet

from typing import TYPE_CHECKING
from apps.app import App

if TYPE_CHECKING:
    from system import System


class Pong(App):
    name = "Pong"

    def __init__(self, system: "System", **kwargs):
        pass

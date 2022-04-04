from typing import Tuple
from typing_extensions import TypeAlias
import pyglet


DisplayCoords: TypeAlias = Tuple[int, int]
RelativeCoords: TypeAlias = Tuple[float, float]


class DisplayWindow(pyglet.window.Window):
    def __init__(self, screen, fullscreen=False):
        super().__init__(resizable=True, screen=screen, fullscreen=fullscreen)

        pyglet.gl.glClearColor(1, 1, 1, 1)

    def from_relative_coords(self, coords: RelativeCoords) -> DisplayCoords:
        return (
            self.relative_width_to_display(coords[0]),
            self.relative_height_to_display(coords[1]),
        )

    def relative_height_to_display(self, height: float) -> int:
        return int(height * self.height)

    def relative_width_to_display(self, width: float) -> int:
        return int(width * self.width)

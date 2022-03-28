from typing import TYPE_CHECKING
import pyglet

from apps.app import App

if TYPE_CHECKING:
    from system import System


class Setup(App):
    def __init__(self):
        self.name = "Setup"

    def init(self, system: "System") -> None:
        self.label = pyglet.text.Label(
            "move this window to display and center in webcam then press space to calibrate",
            font_name="Times New Roman",
            font_size=36,
            x=system.display.width // 2,
            y=system.display.height // 2,
            anchor_x="center",
            anchor_y="center",
            color=(0, 0, 0, 255),
        )

        @system.display.event
        def on_draw():
            self.on_draw(system)

        @system.display.event
        def on_resize(width, height):
            self.label = pyglet.text.Label(
                "move this window to display and center in webcam then press space to calibrate",
                font_name="Times New Roman",
                font_size=36,
                x=system.display.width // 2,
                y=system.display.height // 2,
                anchor_x="center",
                anchor_y="center",
                color=(0, 0, 0, 255),
            )

    def on_draw(self, system):
        system.display.clear()
        self.label.draw()

import pyglet

from system.camera import Camera
from system.displaywindow import DisplayWindow


class System:
    def __init__(self) -> None:
        self.display = DisplayWindow(
            screen=self.get_secondary_screen(), fullscreen=self.has_secondary_screen()
        )
        self.camera = Camera()

    def run(self) -> None:
        pyglet.app.run()

    def get_primary_screen(self):
        return pyglet.canvas.get_display().get_screens()[0]

    def get_secondary_screen(self):
        screens = pyglet.canvas.get_display().get_screens()
        return screens[1] if len(screens) > 1 else screens[0]

    def has_secondary_screen(self):
        return len(pyglet.canvas.get_display().get_screens()) > 1

import pyglet

from apps.app import App
from apps.setup import Setup
from pygarrayimage.arrayimage import ArrayInterfaceImage
from system.camera import Camera
from system.displaywindow import DisplayWindow


class System:
    def __init__(self) -> None:
        self.display = DisplayWindow()
        self.camera = Camera()

    def run(self) -> None:
        pyglet.app.run()

    def camera_image_to_display(self, image, format="BGR"):
        return ArrayInterfaceImage(image, format=format)

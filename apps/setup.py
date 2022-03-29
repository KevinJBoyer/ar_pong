from typing import TYPE_CHECKING
import pyglet

from apps.app import App

if TYPE_CHECKING:
    from system import System


class Setup(App):
    name = "Setup"

    WEBCAM_UPDATE_FREQ_SECONDS = 0.1

    def __init__(self, system: "System", apps: list[App]):
        self.system = system
        self.apps = apps

        self.label = self.make_instructions()

        self.camera_window = pyglet.window.Window(
            width=self.system.camera.width, height=self.system.camera.height
        )

        self.system.display.push_handlers(
            on_draw=self.display_draw, on_resize=self.display_resize
        )
        self.camera_window.push_handlers(on_draw=self.camera_draw)

        pyglet.clock.schedule_interval(self.update, self.WEBCAM_UPDATE_FREQ_SECONDS)

    def update(self, delta_seconds):
        self.camera_window.switch_to()
        self.camera_draw()

    def display_draw(self):
        self.system.display.clear()
        self.label.draw()

    def display_resize(self, width, height):
        self.label = self.make_instructions()

    def camera_draw(self):
        camera_image = self.system.camera.get_image()
        pyglet_image = self.system.camera_image_to_display(camera_image)
        pyglet_image.blit(0, 0)

    def make_instructions(self):
        return pyglet.text.Label(
            "move this window to display\nand center in webcam,\nthen press space to calibrate",
            font_name="Times New Roman",
            font_size=36,
            x=self.system.display.width // 2,
            y=self.system.display.height // 2,
            anchor_x="center",
            anchor_y="center",
            align="center",
            color=(0, 0, 0, 255),
            multiline=True,
            width=self.system.display.width,
        )

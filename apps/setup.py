from enum import Enum, auto
from typing import TYPE_CHECKING
import pyglet

from apps.app import App

if TYPE_CHECKING:
    from system import System


class SetupState(Enum):
    USER_SETUP = auto()
    CALIBRATING = auto()
    CALIBRATION_FAILED = auto()
    RUNNING_APP = auto()


class Setup(App):
    name = "Setup"

    MARKER_MIN_SIZE = 100
    MARKER_MAX_SIZE = 500
    MAX_CALIBRATION_TIME_SECONDS = 3.0

    WEBCAM_UPDATE_FREQ_SECONDS = 1.0 / 10
    DISPLAY_UPDATE_FREQ_SECONDS = 1.0 / 30

    def __init__(self, system: "System", apps: list[App]):
        self.state = SetupState.USER_SETUP

        self.system = system
        self.apps = apps

        self.label = self.make_instructions()

        self.system.display.push_handlers(
            on_draw=self.display_draw,
            on_key_press=self.on_key_press,
        )

        self.camera_window = pyglet.window.Window(
            width=self.system.camera.width,
            height=self.system.camera.height,
            screen=self.system.get_primary_screen(),
        )
        self.camera_window.set_location(0, 0)
        self.camera_window.push_handlers(
            on_draw=self.camera_draw, on_key_press=self.on_key_press
        )

        pyglet.clock.schedule_interval(
            self.camera_draw, self.WEBCAM_UPDATE_FREQ_SECONDS
        )

        pyglet.clock.schedule_interval(
            self.display_update, self.DISPLAY_UPDATE_FREQ_SECONDS
        )

    def get_marker_images(self, marker_size):
        markers = self.system.camera.get_calibration_markers(size=marker_size)
        return [
            self.system.camera_image_to_display(marker, format="I")
            for marker in markers
        ]

    def display_draw(self):
        self.system.display.clear()
        self.label = self.make_instructions()
        self.label.draw()

        if self.state == SetupState.CALIBRATING:
            window_width, window_height = self.system.display.get_size()
            marker_width = self.marker_images[0].width
            marker_height = self.marker_images[0].height

            self.marker_images[0].blit(0, window_height - marker_height)
            self.marker_images[1].blit(
                window_width - marker_width, window_height - marker_height
            )
            self.marker_images[2].blit(window_width - marker_width, 0)
            self.marker_images[3].blit(0, 0)

    def on_key_press(self, symbol, modifiers):
        if (
            self.state in (SetupState.USER_SETUP, SetupState.CALIBRATION_FAILED)
            and symbol == pyglet.window.key.SPACE
        ):
            self.state = SetupState.CALIBRATING

    def display_update(self, delta_seconds):
        if self.state in (SetupState.USER_SETUP, SetupState.CALIBRATION_FAILED):
            self.marker_size = self.MARKER_MIN_SIZE

        elif self.state == SetupState.CALIBRATING:
            marker_delta = (self.MARKER_MAX_SIZE - self.MARKER_MIN_SIZE) / (
                self.MAX_CALIBRATION_TIME_SECONDS / self.DISPLAY_UPDATE_FREQ_SECONDS
            )
            self.marker_size += int(marker_delta)
            self.marker_images = self.get_marker_images(self.marker_size)

            if self.marker_size > self.MARKER_MAX_SIZE:
                self.state = SetupState.CALIBRATION_FAILED

    def camera_draw(self, delta_seconds=None):
        self.camera_window.switch_to()
        camera_image = self.system.camera.get_image()
        pyglet_image = self.system.camera_image_to_display(camera_image)

        # why is the returned image backward?
        flipped_image = pyglet_image.get_texture().get_transform(
            flip_x=True, flip_y=True
        )
        flipped_image.blit(flipped_image.width, flipped_image.height)

    def make_instructions(self):
        if self.state == SetupState.CALIBRATING:
            message = "calibrating..."
        elif self.state == SetupState.CALIBRATION_FAILED:
            message = "calibration failed\npress space to try again"
        else:
            message = "move this window to display\nand center in webcam,\nthen press space to calibrate"

        return pyglet.text.Label(
            message,
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

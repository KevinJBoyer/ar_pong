import pyglet
from system.camerawindow import CameraWindow

from system.system import System


class Setup:
    name = "Setup"

    SKIP_CALIBRATION = False

    CAMERA_UPDATE_FREQ_SECONDS = 1.0 / 5
    MARKER_PADDING = 0.05
    MARKER_SIZE = 0.25

    def __init__(self, system: System, apps: list):

        self.system = system
        self.apps = apps

        self.camera_window = CameraWindow(self.system)

        self.system.display.push_handlers(
            on_draw=self.display_draw,
            on_key_press=self.on_key_press,
        )

        pyglet.clock.schedule_interval(
            self.check_for_calibration, self.CAMERA_UPDATE_FREQ_SECONDS
        )

    def check_for_calibration(self, delta_time_seconds):
        camera_image = self.system.camera.get_image()

        # Attempt to calibrate
        left, right, bottom, top = self.get_marker_positions()
        marker_width = self.marker_images[0].width
        marker_height = self.marker_images[0].height
        marker_corners = [
            (left, top + marker_height),
            (right + marker_width, top + marker_height),
            (right + marker_width, bottom),
            (left, bottom),
        ]
        self.system.camera.calibrate(camera_image, marker_corners)

        self.camera_window.draw_camera_image(camera_image)

        if self.system.camera.homography is not None or Setup.SKIP_CALIBRATION:
            self.launch_app()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.Q:
            pyglet.app.exit()

    def display_draw(self):
        self.system.display.clear()

        display_marker_size = self.system.display.relative_height_to_display(
            Setup.MARKER_SIZE
        )
        self.marker_images = [
            self.system.camera.image_to_display(marker, format="I")
            for marker in self.system.camera.get_calibration_markers(
                size=display_marker_size
            )
        ]

        pyglet.text.Label(
            "calibrating...",
            font_name="Times New Roman",
            font_size=36,
            x=self.system.display.width // 2,
            y=self.system.display.height // 2,
            anchor_x="center",
            anchor_y="center",
            align="center",
            color=(0, 0, 0, 255),
        ).draw()

        left, right, bottom, top = self.get_marker_positions()
        self.marker_images[0].blit(left, top)
        self.marker_images[1].blit(right, top)
        self.marker_images[2].blit(right, bottom)
        self.marker_images[3].blit(left, bottom)

    def get_marker_positions(self):
        """Get positions to place the markers in display coordinates."""

        window_width, window_height = self.system.display.get_size()
        marker_width = self.marker_images[0].width
        marker_height = self.marker_images[0].height

        display_padding = self.system.display.relative_height_to_display(
            Setup.MARKER_PADDING
        )

        left = display_padding
        right = window_width - marker_width - display_padding
        bottom = display_padding
        top = window_height - marker_height - display_padding

        return left, right, bottom, top

    def launch_app(self):
        pyglet.clock.unschedule(self.check_for_calibration)
        self.system.display.pop_handlers()
        self.camera_window.set_visible(visible=False)
        self.camera_window.close()
        self.camera_window = None

        if len(self.apps) == 1:
            self.running_app = self.apps[0](self.system)
        else:
            # future: show an app selection menu
            self.running_app = self.apps[0](self.system)

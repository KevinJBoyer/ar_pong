from typing import Optional
import pyglet

from system.system import System


class CameraWindow(pyglet.window.Window):
    DEFAULT_UPDATE_FREQ_SECONDS = 1.0 / 5

    def __init__(self, system: System, update_freq_seconds: Optional[float] = None):
        self.system = system
        self.image = None

        super().__init__(
            width=self.system.camera.width,
            height=self.system.camera.height,
            screen=self.system.get_primary_screen(),
        )
        self.set_location(0, 0)

        pyglet.gl.glClearColor(1, 1, 1, 1)

        self.push_handlers(on_key_press=self.on_key_press)

        self.camera_image = None

    def close(self):
        self.pop_handlers()
        super().close()

    def draw_camera_image(self, camera_image=None):
        if camera_image is not None:
            image = self.system.camera.image_to_display(camera_image)
            self.camera_image = image.get_transform(flip_x=True)

        self.on_draw()

    def on_draw(self, delta_seconds=None):
        self.switch_to()

        if self.camera_image is not None:
            self.camera_image.blit(self.camera_image.width, 0)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.Q:
            pyglet.app.exit()

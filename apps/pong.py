from dataclasses import dataclass

import pyglet

from common.handstracker import HandsTracker
from system.camerawindow import CameraWindow
from system.system import System


@dataclass
class Paddle:
    system: System

    x: float = 0.0
    y: float = 0.5

    WIDTH: float = 0.05
    HEIGHT: float = 0.15
    COLOR = (0, 0, 0)
    SPEED = 0.02

    def draw(self):
        x, y = self.system.display.from_relative_coords((self.x, self.y))
        width = self.system.display.relative_width_to_display(Paddle.WIDTH)
        height = self.system.display.relative_height_to_display(Paddle.HEIGHT)

        shape = pyglet.shapes.Rectangle(x, y, width, height, self.COLOR)
        shape.anchor_x = self.WIDTH / 2
        shape.anchor_y = self.HEIGHT / 2
        shape.draw()


@dataclass
class Ball:
    system: System

    x: float = 0.3
    y: float = 0.5
    dx: float = 1.0
    dy: float = 1.0
    speed: float = 0.1

    SIZE: float = 0.025
    COLOR = (0, 0, 0)

    def draw(self):
        x, y = self.system.display.from_relative_coords((self.x, self.y))
        size = self.system.display.relative_height_to_display(Ball.SIZE)
        pyglet.shapes.Circle(x, y, size, color=Ball.COLOR).draw()

    def update(self, delta_time_seconds, left_paddle, right_paddle) -> bool:
        self.x += self.dx * delta_time_seconds * self.speed
        self.y += self.dy * delta_time_seconds * self.speed

        if self.y < Ball.SIZE:
            self.dy = 1
        elif self.y > 1.0 - Ball.SIZE:
            self.dy = -1

        if self.x < Paddle.WIDTH:
            if self.y > left_paddle.y and self.y < left_paddle.y + Paddle.HEIGHT:
                self.dx = 1
            else:
                return False

        if self.x > 1.0 - Paddle.WIDTH:
            if self.y > right_paddle.y and self.y < right_paddle.y + Paddle.HEIGHT:
                self.dx = -1
            else:
                return False

        return True


class Pong:
    name = "Pong"

    SHOW_CAMERA = False  # True

    CAMERA_UPDATE_FREQ_SECONDS = 1.0 / 5
    TRACK_HANDS_FREQ_SECONDS = 1.0 / 5
    UPDATE_FREQ_SECONDS = 1.0 / 30

    def __init__(self, system: System):
        self.system = system

        self.hands = HandsTracker(
            model_complexity=0,
            min_tracking_confidence=0.1,
            fadein_threshold=0.25,
            fadeout_threshold=2.0,
            interpolation_speed=0.2,
            exclusion_radius=0.25,
        )

        self.camera_image = None

        self.key_up = False
        self.key_down = False
        self.key_w = False
        self.key_s = False

        self.system.display.push_handlers(
            on_draw=self.draw,
            on_key_press=self.on_key_press,
            on_key_release=self.on_key_release,
        )

        if Pong.SHOW_CAMERA:
            self.init_camera_window()

        pyglet.clock.schedule_interval(self.track_hands, self.TRACK_HANDS_FREQ_SECONDS)
        pyglet.clock.schedule_interval(self.update, self.UPDATE_FREQ_SECONDS)

        self.reset_game()

    def init_camera_window(self):
        self.fps_display = pyglet.window.FPSDisplay(window=self.system.display)

        self.camera_window = CameraWindow(self.system)

        def draw_camera(delta_time_seconds=None):
            self.camera_window.draw_camera_image(self.camera_image)
            self.fps_display.draw()

        pyglet.clock.schedule_interval(draw_camera, self.CAMERA_UPDATE_FREQ_SECONDS)

    def reset_game(self):
        self.ball = Ball(system=self.system)
        self.ball.dy = self.system.display.height / self.system.display.width
        self.left_paddle = Paddle(system=self.system)
        self.right_paddle = Paddle(system=self.system)
        self.right_paddle.x = 1.0 - Paddle.WIDTH

    def draw(self):
        self.system.display.switch_to()
        self.system.display.clear()

        self.ball.draw()
        self.left_paddle.draw()
        self.right_paddle.draw()

        """
        self.hands.update_current_locations()
        for hand in self.hands.get():
            coords = hand.current_location
            if coords is not None:
                coords = self.relative_coords_to_display(coords)
                pyglet.shapes.Circle(
                    coords[0], coords[1], Ball.SIZE, color=Ball.COLOR
                ).draw()
        """

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.Q:
            pyglet.app.exit()
        elif symbol == pyglet.window.key.UP:
            self.key_up = True
        elif symbol == pyglet.window.key.DOWN:
            self.key_down = True
        elif symbol == pyglet.window.key.W:
            self.key_w = True
        elif symbol == pyglet.window.key.S:
            self.key_s = True

    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            self.key_up = False
        elif symbol == pyglet.window.key.DOWN:
            self.key_down = False
        elif symbol == pyglet.window.key.W:
            self.key_w = False
        elif symbol == pyglet.window.key.S:
            self.key_s = False

    def update(self, delta_time_seconds):
        self.update_paddles_from_keys()
        self.ball.update(delta_time_seconds, self.left_paddle, self.right_paddle)
        self.draw()

    def update_paddles_from_keys(self):
        if self.key_w:
            self.left_paddle.y += Paddle.SPEED
        elif self.key_s:
            self.left_paddle.y -= Paddle.SPEED

        if self.key_up:
            self.right_paddle.y += Paddle.SPEED
        elif self.key_down:
            self.right_paddle.y -= Paddle.SPEED

    """
    def update_paddles(self):
        window_width, _ = self.system.display.get_size()

        self.hands.update_current_locations()
        hands_coords = [
            self.relative_coords_to_display(hand.current_location)
            for hand in self.hands.get()
            if hand.current_location is not None
        ]

        for hand_coords in hands_coords:
            if hand_coords < window_width / 2:
                self.left_paddle.x += (
                    hand_coords[0] - self.left_paddle.x
                ) * Paddle.SPEED
                self.left_paddle.y += (
                    hand_coords[1] - self.left_paddle.y
                ) * Paddle.SPEED

            elif hand_coords > window_width / 2:
                self.right_paddle.x += (
                    hand_coords[0] - self.left_paddle.x
                ) * Paddle.SPEED
                self.right_paddle.y += (
                    hand_coords[1] - self.left_paddle.y
                ) * Paddle.SPEED
    """

    def track_hands(self, delta_time_seconds):
        self.camera_image = self.system.camera.get_image()
        self.hands.update_detected_locations(self.camera_image)
        self.hands.draw(self.camera_image)

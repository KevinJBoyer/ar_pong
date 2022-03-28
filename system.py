from enum import Enum, auto
from pickletools import pylist
from typing import Callable, Tuple
from typing_extensions import TypeAlias

import pyglet

from apps.app import App
from apps.setup import Setup
from camera import Camera

SchedulableFunction: TypeAlias = Callable[["System", float], None]


class System:
    def __init__(self, apps: list[App]) -> None:
        self.apps = apps

        self.display = pyglet.window.Window(resizable=True)
        self.camera = Camera()

        self.scheduled_fns: list[Tuple[SchedulableFunction, float]] = []

        pyglet.gl.glClearColor(1, 1, 1, 1)

    def schedule(self, function: SchedulableFunction, frequency_seconds: float):
        self.scheduled_fns.append((function, frequency_seconds))

        pyglet.clock.schedule_interval(lambda dt: function(self, dt), frequency_seconds)

    def run(self) -> None:
        setup = Setup()
        setup.init(self, self.apps)
        pyglet.app.run()

import pyglet


class DisplayWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(resizable=True)

        pyglet.gl.glClearColor(1, 1, 1, 1)

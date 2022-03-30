import pyglet


class DisplayWindow(pyglet.window.Window):
    def __init__(self, screen, fullscreen):
        super().__init__(resizable=True, screen=screen, fullscreen=fullscreen)

        pyglet.gl.glClearColor(1, 1, 1, 1)

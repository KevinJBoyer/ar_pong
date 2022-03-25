import pyglet
from pyglet.window import key
from pygarrayimage.arrayimage import ArrayInterfaceImage

from camera import Camera, Corners


def render_markers(window, marker_images):
    window_width, window_height = window.get_size()
    marker_width = marker_images[0].width
    marker_height = marker_images[0].height

    marker_images[0].blit(0, window_height - marker_height)
    marker_images[1].blit(window_width - marker_width, window_height - marker_height)
    marker_images[2].blit(window_width - marker_width, 0)
    marker_images[3].blit(0, 0)


camera = Camera()
markers = camera.get_calibration_markers()
marker_images = [ArrayInterfaceImage(marker, format="I") for marker in markers]

pyglet.gl.glClearColor(1, 1, 1, 1)
projection_window = pyglet.window.Window(resizable=True)


@projection_window.event
def on_draw():
    projection_window.clear()
    render_markers(projection_window, marker_images)


"""
camera_window = pyglet.window.Window(width=camera.width, height=camera.height)

@camera_window.event
def on_draw():
    camera_window.clear()
    camera_image = camera.get_image()

    pyglet_image = ArrayInterfaceImage(camera_image, format="BGR")

    pyglet_image.blit(0, 0)

    fps_display.draw()
"""


@projection_window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        image = camera.get_image()

        window_width, window_height = projection_window.get_size()
        screen_corners: Corners = [
            (0.0, window_height),
            (window_width, window_height),
            (window_width, 0.0),
            (0.0, 0.0),
        ]

        camera.calibrate(image, screen_corners)
        print(camera.homography)


def update(dt):
    on_draw()


pyglet.clock.schedule_interval(update, 0.1)

# fps_display = pyglet.window.FPSDisplay(window=camera_window)

pyglet.app.run()


# create camera
# draw markers
# calibrate camera

# success?
#   create hands tracker
#   feed camera -> hands tracker
#   draw hands
#   loop
"""
User states-
    1. Set up
        a. User selects webcam
        b. User moves screen to correct physical device
        c. User aims webcam at screen (user needs to be able to see contents of webcam?)
        d. User presses input when ready to calibrate
    2. Calibrate
        a. Program displays markers from camera and calls camera.calibrate()
        b. If calibration fails, go to 1.b
    3. 
        

"""

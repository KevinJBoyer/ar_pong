import pyglet

from camera import Camera


def marker_to_pyglet_image(marker):
    height, width = marker.shape
    number_of_channels = 1
    number_of_bytes = height * width * number_of_channels

    marker = marker.ravel()

    image_texture = (pyglet.gl.GLubyte * number_of_bytes)(*marker.astype("uint8"))

    return pyglet.image.ImageData(width, height, "I", image_texture)


window = pyglet.window.Window(resizable=True)
pyglet.gl.glClearColor(1, 1, 1, 1)

camera = Camera(camera_id="test.png")
camera.set_homography()
markers = camera.get_homography_markers()
marker_images = [marker_to_pyglet_image(marker) for marker in markers]


def render_markers(window, marker_images):
    window_width, window_height = window.get_size()
    marker_width = marker_images[0].width
    marker_height = marker_images[0].height

    marker_images[0].blit(0, window_height - marker_height)
    marker_images[1].blit(window_width - marker_width, window_height - marker_height)
    marker_images[2].blit(window_width - marker_width, 0)
    marker_images[3].blit(0, 0)


# create camera
# draw markers
# calibrate camera

# success?
#   create hands tracker
#   feed camera -> hands tracker
#   draw hands
#   loop


@window.event
def on_draw():

    window.clear()
    render_markers(window, marker_images)


# pyglet.app.run()

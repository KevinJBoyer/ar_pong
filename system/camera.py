from typing import Any, Optional, Tuple
from typing_extensions import TypeAlias
import cv2
import numpy as np

from pygarrayimage.arrayimage import ArrayInterfaceImage

CameraCoords: TypeAlias = Tuple[float, float]
DisplayCoords: TypeAlias = Tuple[int, int]
RelativeCoords: TypeAlias = Tuple[float, float]


class Camera:
    DEBUG = False

    MARKER_DICTIONARY = cv2.aruco.DICT_7X7_50
    MARKER_SIZE: int = 300

    def __init__(self, camera_id: int = 0):
        self.camera_id = camera_id
        self.camera = cv2.VideoCapture(camera_id)

        self.width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.aruco_dict = cv2.aruco.Dictionary_get(Camera.MARKER_DICTIONARY)

        self.homography = None

    def _find_markers(self, image) -> Tuple[Any, list[int]]:
        marker_corners, marker_ids, rejected_markers = cv2.aruco.detectMarkers(
            image, self.aruco_dict
        )

        if self.DEBUG:
            cv2.aruco.drawDetectedMarkers(
                image, rejected_markers, borderColor=(100, 0, 240)
            )
            cv2.aruco.drawDetectedMarkers(image, marker_corners, marker_ids)

        if marker_ids is not None:
            marker_ids = [id for [id] in marker_ids]
            return marker_corners, marker_ids
        else:
            return (None, [])

    def _find_projection_corners(self, image) -> Optional[list[CameraCoords]]:
        marker_corners, ids = self._find_markers(image)

        if len(ids) != 4:
            return None

        projection_corners: list[CameraCoords] = [
            (0.0, 0.0),
            (0.0, 0.0),
            (0.0, 0.0),
            (0.0, 0.0),
        ]

        for idx, id in enumerate(ids):
            corner = id
            marker_corner: CameraCoords = marker_corners[idx][0][corner]
            projection_corners[id] = marker_corner

        return projection_corners

    def get_image(self):
        success, image = self.camera.read()
        return image

    def get_calibration_markers(self, size=None) -> list:
        """
        Return a list of four calibration marker images:
        [TopLeft, TopRight, BottomRight, BottomLeft]
        """

        if size is None:
            size = Camera.MARKER_SIZE

        return [cv2.aruco.drawMarker(self.aruco_dict, id, size) for id in range(4)]

    def calibrate(self, image, display_corners: list[DisplayCoords]) -> bool:
        projection_corners = self._find_projection_corners(image)

        if projection_corners is not None:
            self.homography, _ = cv2.findHomography(
                np.array(projection_corners), np.array(display_corners)
            )

        return projection_corners is not None

    def image_to_display(self, image, format="BGR"):
        """Tranform an image returned by CV2 to a pyglet.TextureRegion."""

        # future: modify ArrayInterfaceImage so that we don't need to flip the
        # results over the y-axis
        texture_region = (
            ArrayInterfaceImage(image, format=format)
            .get_texture()
            .get_transform(flip_y=True)
        )
        texture_region.anchor_y = 0
        return texture_region

    def coords_to_display(self, coords: CameraCoords) -> Optional[DisplayCoords]:
        """Transform coordinates in the camera to the equivalent coordinates on the display."""

        if self.homography is None:
            return None

        homogenous_camera_coords = np.array([coords[0], coords[1], 1])
        homogenous_display_coords = self.homography @ homogenous_camera_coords
        cartesian_display_coords = (
            int(homogenous_display_coords[0] / homogenous_display_coords[2]),
            int(homogenous_display_coords[1] / homogenous_display_coords[2]),
        )

        return cartesian_display_coords

    def from_relative_coords(self, coords: RelativeCoords) -> CameraCoords:
        return (coords[0] * self.width, coords[1] * self.height)

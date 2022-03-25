from typing import Any, Optional, Tuple, cast
from typing_extensions import TypeAlias
import cv2
import numpy as np

Corner: TypeAlias = Tuple[float, float]
Corners: TypeAlias = list[Corner]


class Camera:
    MARKER_DICTIONARY = cv2.aruco.DICT_7X7_50
    MARKER_SIZE: int = 300

    def __init__(self, camera_id=0):
        self.camera_id: int = camera_id
        self.camera = cv2.VideoCapture(camera_id)

        self.height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)

        self.aruco_dict = cv2.aruco.Dictionary_get(Camera.MARKER_DICTIONARY)

        self.homography = None

    def _find_markers(self, image) -> Tuple[Any, list[int]]:
        image = cv2.flip(image, 1)  # why is this needed?!
        marker_corners, marker_ids, rejected_markers = cv2.aruco.detectMarkers(
            image, self.aruco_dict
        )
        marker_ids = [id for [id] in marker_ids]
        return marker_corners, marker_ids

    def _find_projection_corners(self, image) -> Optional[Corners]:
        marker_corners, ids = self._find_markers(image)

        if len(ids) != 4:
            return None

        projection_corners: Corners = [(0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)]

        for id in ids:
            corner = id
            marker_corner: Corner = marker_corners[id][0][corner]
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

    def calibrate(self, image, screen_corners: Corners) -> bool:
        projection_corners = self._find_projection_corners(image)

        if projection_corners is not None:
            self.homography, success = cv2.findHomography(
                np.array(projection_corners), np.array(screen_corners)
            )
            return success

        return False

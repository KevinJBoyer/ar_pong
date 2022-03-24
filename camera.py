from typing import Any, Optional, Tuple
from typing_extensions import TypeAlias
import cv2

Corners: TypeAlias = Tuple[
    Tuple[float, float],
    Tuple[float, float],
    Tuple[float, float],
    Tuple[float, float],
]


class Camera:
    MARKER_DICTIONARY = cv2.aruco.DICT_7X7_50
    MARKER_SIZE: int = 300

    # todo - I think this should be set by pyglet module, doesn't make sense to have defaults here
    SCREEN_CORNERS: Corners = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))

    def __init__(self, camera_id=0):
        self.camera_id: int = camera_id
        self.camera = cv2.VideoCapture(camera_id)

        self.height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)

        self.aruco_dict = cv2.aruco.Dictionary_get(Camera.MARKER_DICTIONARY)

        self.homography = None

    def _find_markers(self) -> Tuple[Any, list[int]]:
        image = self.get_image()
        image = cv2.flip(image, 1)  # why is this needed?!
        corners, ids, rejected = cv2.aruco.detectMarkers(image, self.aruco_dict)
        return corners, ids

    def _find_projection_corners(self) -> Optional[Corners]:
        corners, ids = self._find_markers()
        if len(ids) != 4:
            return None

        # todo
        print(corners, ids)

        return None

    def get_image(self):
        success, image = self.camera.read()
        return image

    def get_homography_markers(self, size=None) -> list:
        if size is None:
            size = Camera.MARKER_SIZE

        return [cv2.aruco.drawMarker(self.aruco_dict, id, size) for id in range(4)]

    def set_homography(self, dest_corners: Optional[Corners] = None) -> bool:
        if dest_corners is None:
            dest_corners = Camera.SCREEN_CORNERS

        src_corners = self._find_projection_corners()

        if src_corners is not None:
            self.homography, success = cv2.findHomography(src_corners, dest_corners)
            return success

        return False

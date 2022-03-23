import cv2


class Camera:
    MARKER_DICTIONARY = cv2.aruco.DICT_7X7_50
    MARKER_SIZE = 300

    def __init__(self, camera_id=0):
        self.camera_id: int = camera_id
        self.camera = cv2.VideoCapture(camera_id)

        self.height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)

        self.homography = None

    def get_image(self):
        success, img = self.camera.read()
        return img

    def get_homography_markers(self):
        arucoDict = cv2.aruco.Dictionary_get(Camera.MARKER_DICTIONARY)
        return [
            cv2.aruco.drawMarker(arucoDict, id, Camera.MARKER_SIZE) for id in range(4)
        ]

    def set_homography(self, src_corners, dest_corners):
        # todo this should take dest_corners only and find the markers itself
        self.homography, success = cv2.findHomography(src_corners, dest_corners)

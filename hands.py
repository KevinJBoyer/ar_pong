from math import sqrt
from typing import NamedTuple, Optional, Tuple
import mediapipe as mp

from typing_extensions import TypeAlias

Point = NamedTuple("Point", [("x", int), ("y", int)])
Distance: TypeAlias = float
CoordsIndex: TypeAlias = int

"""
todo: add tracking logic to Hand()
todo: add unit tests
todo: add interpolation for smooth coordinate changes
todo: abstract out from HandTracker to ObjectTracker
"""

class HandTracker:
    TRACKING_LANDMARK = mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP

    def __init__(self, num_hands: int = 2):
        self.hands = [Hand() for _ in range(num_hands)]

        self.mp_hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.1,  # 0.05,
            min_tracking_confidence=0.8,  # 0.05,
        )

    def update(self, img) -> None:
        detected_hands = self.mp_hands.process(img).multi_hand_landmarks

        if detected_hands is None:
            return

        coords: list[Point] = []
        for hand_coords in detected_hands:
            x = hand_coords.landmark[self.TRACKING_LANDMARK].x
            y = hand_coords.landmark[self.TRACKING_LANDMARK].y
            coords.append(Point(x, y))

        # if we've detected all the hands, update based on which is closest to which
        if len(coords) >= len(self.hands):
            for hand in self.hands:
                hand.update(coords)

        # if we've only detected some hands, figure out which hands are closest
        # to the detected coords and update those
        else:
            pass


class Hand:
    def __init__(self):
        # the last location we detected the person's hand at
        # tuple (x, y) | None
        self.detected_location: Optional[Point] = None

    def dist(self, point: Point) -> Optional[Distance]:
        if self.detected_location is not None:
            return sqrt(
                (point.x - self.detected_location.x) ** 2
                + (point.y - self.detected_location.y) ** 2
            )
        return None

    def closest_coords(self, coords) -> Optional[Tuple[CoordsIndex, Distance]]:
        """return (coords_idx, distance) of the closest coords to these hands"""
        if self.detected_location is None:
            return None

        closest_idx: CoordsIndex = 0
        closest_dist: Distance = self.dist(coords[0])

        for idx, point in enumerate(coords[1:]):
            dist = self.dist(point)
            if dist < closest_dist:
                closest_idx = idx
                closest_dist = dist

        return (closest_idx, closest_dist)

    # change our detected_location to the closest coords and then remove those
    # from the coords list
    def update(self, coords: list[Point]) -> None:
       # closest_idx
        #_: Distance
        closest_idx: CoordsIndex, _: = self.closest_coords(coords)
        self.detected_location = coords[closest_idx]
        coords.pop(closest_idx)

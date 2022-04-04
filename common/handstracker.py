from typing import Any, Optional

import mediapipe as mp

from common.objecttracker.multiobjecttracker import MultiObjectTracker
from common.objecttracker.point import Point


class HandsTracker:
    def __init__(
        self,
        model_complexity=1,
        min_detection_confidence=0.1,
        min_tracking_confidence=0.8,
        **kwargs,
    ):
        # the specific landmark in the model hand to center the hand
        self.tracking_landmark = mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP

        self.tracked_hands = MultiObjectTracker(**kwargs)

        self.mp_detected_hands: Optional[Any] = None
        self.mp_hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def get(self, index: Optional[int] = None) -> Optional[Point]:
        if index is None:
            return self.tracked_hands.object_trackers
        elif index < len(self.tracked_hands.object_trackers):
            return self.tracked_hands.object_trackers[index].current_location

        return None

    def update(self, image) -> None:
        self.update_detected_locations(image)
        self.update_current_locations()

    def update_detected_locations(self, image):
        self.mp_detected_hands = self.mp_hands.process(image).multi_hand_landmarks

        coords: list[Point] = []

        if self.mp_detected_hands is not None:
            for hand_coords in self.mp_detected_hands:
                x = hand_coords.landmark[self.tracking_landmark].x
                y = hand_coords.landmark[self.tracking_landmark].y
                coords.append(Point(x, y))

        self.tracked_hands.update_detected_locations(coords)

    def update_current_locations(self):
        self.tracked_hands.update_current_locations()

    def draw(self, image) -> None:
        if self.mp_detected_hands is not None:
            for hand_landmarks in self.mp_detected_hands:
                mp.solutions.drawing_utils.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS,
                    mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                    mp.solutions.drawing_styles.get_default_hand_connections_style(),
                )

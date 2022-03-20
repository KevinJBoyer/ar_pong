from typing import Any, Optional

import mediapipe as mp

from objecttracker.multiobjecttracker import MultiObjectTracker
from objecttracker.point import Point


class HandsTracker:
    # the specific landmark in the model hand to center the hand
    tracking_landmark = mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP

    # accuracy vs. latency settings for mp.solutions.hands.Hands
    model_complexity = 1
    min_detection_confidence = 0.1
    min_tracking_confidence = 0.8

    tracked_hands: MultiObjectTracker
    detected_hands: Optional[Any] = None

    def __init__(self):
        self.tracked_hands = MultiObjectTracker(num_objects=2)

        self.mp_hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            model_complexity=self.model_complexity,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )

    def update(self, img) -> None:
        self.detected_hands = self.mp_hands.process(img).multi_hand_landmarks

        coords: list[Point] = []

        if self.detected_hands is not None:
            for hand_coords in self.detected_hands:
                x = hand_coords.landmark[self.tracking_landmark].x
                y = hand_coords.landmark[self.tracking_landmark].y
                coords.append(Point(x, y))

        self.tracked_hands.update_detected_locations(coords)
        self.tracked_hands.update_current_locations()

    def draw(self, img) -> None:
        if self.detected_hands is not None:
            for hand_landmarks in self.detected_hands:
                mp.solutions.drawing_utils.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS,
                    mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                    mp.solutions.drawing_styles.get_default_hand_connections_style(),
                )

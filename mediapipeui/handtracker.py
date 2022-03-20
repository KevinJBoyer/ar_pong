from math import sqrt
from typing import Any, NamedTuple, Optional, Tuple
import mediapipe as mp

from typing_extensions import TypeAlias

from . import Point

from .detectedobject import DetectedObject

# todo: generalize to generic objects
# todo: add tests
# todo: generalize to multiple generic objects


class HandTracker:
    # the specific landmark in the model hand to center the hand
    tracking_landmark = mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP

    # accuracy vs. latency settings for mp.solutions.hands.Hands
    model_complexity = 1
    min_detection_confidence = 0.1
    min_tracking_confidence = 0.8

    hand: DetectedObject
    detected_hands: Optional[Any] = None

    def __init__(self):
        self.hand = DetectedObject()

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

        self.hand.update_detected_location(coords)
        self.hand.update_current_location()

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

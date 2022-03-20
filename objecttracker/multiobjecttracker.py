from .point import Point
from .trackedobject import TrackedObject


class MultiObjectTracker:
    def __init__(self, num_objects: int, **kwargs):
        self.tracked_objects = [TrackedObject(**kwargs) for _ in range(num_objects)]

    # todo: Formally, what this should REALLY do is solve the assignment
    # problem... but setting a detection radius is good enough for now.
    def update_detected_locations(self, candidates: list[Point]):
        for tracked_object in self.tracked_objects:
            detected_location = tracked_object.update_detected_location(candidates)

            # If a candidate location was picked, remove it so another tracked
            # object doesn't try to also assign itself to that location.
            if detected_location is not None:
                candidates.remove(detected_location)

    def update_current_locations(self):
        for tracked_object in self.tracked_objects:
            tracked_object.update_current_location()

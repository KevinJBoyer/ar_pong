from .point import Point
from .objecttracker import ObjectTracker


class MultiObjectTracker:
    def __init__(self, num_objects: int, **kwargs):
        self.object_trackers = [ObjectTracker(**kwargs) for _ in range(num_objects)]

    # todo: formally, what this should REALLY do is solve the assignment
    # problem... but setting a detection radius is good enough for now.
    def update_detected_locations(self, candidates: list[Point]):
        for object_tracker in self.object_trackers:
            detected_location = object_tracker.update_detected_location(candidates)

            # If a candidate location was picked, remove it so another tracked
            # object doesn't try to also assign itself to that location.
            if detected_location is not None:
                candidates.remove(detected_location)

    def update_current_locations(self):
        for object_tracker in self.object_trackers:
            object_tracker.update_current_location()

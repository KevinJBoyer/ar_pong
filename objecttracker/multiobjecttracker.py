from .point import Point
from .objecttracker import ObjectTracker


class MultiObjectTracker:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.object_trackers: list[ObjectTracker] = []

    # todo: formally, what this should REALLY do is solve the assignment
    # problem... but setting a detection radius is good enough for now.
    def update_detected_locations(self, candidates: list[Point]):
        # object_tracker_queue: list[ObjectTracker] = []
        # object_tracker_queue.append(object_tracker)

        # If we have more unassigned locations than object trackers,
        # create more object trackers.
        while len(candidates) > len(self.object_trackers):
            object_tracker = ObjectTracker(**self.kwargs)
            self.object_trackers.append(object_tracker)

        for object_tracker in self.object_trackers:
            detected_location = object_tracker.update_detected_location(candidates)

            # If a candidate location was picked, remove it so another tracked
            # object doesn't try to also assign itself to that location.
            if detected_location is not None:
                candidates.remove(detected_location)

            # If a candidate location wasn't picked and the tracker has faded
            # out, remove it so we don't keep processing over it.
            elif object_tracker.fadeout_progress() > 1.0:
                self.object_trackers.remove(object_tracker)

    def update_current_locations(self):
        for object_tracker in self.object_trackers:
            object_tracker.update_current_location()

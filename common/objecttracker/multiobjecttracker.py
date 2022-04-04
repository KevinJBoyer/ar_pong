from .point import Point
from .objecttracker import ObjectTracker


class MultiObjectTracker:
    def __init__(self, exclusion_radius=0.0, **kwargs):
        self.kwargs = kwargs
        self.object_trackers: list[ObjectTracker] = []

        # If an object tracker picks a candidate location, all other locations
        # in the exclusion radius are removed (so another object tracker
        # won't pick them up). Set to 0.0 for no exclusion radius.
        self.exclusion_radius = exclusion_radius

    # todo: Formally, what this should REALLY do is solve the assignment
    # problem... but setting a detection radius is good enough for now.
    def update_detected_locations(self, candidates: list[Point]):

        """
        todo: Even this implementation has a subtle bug. Consider if a
        signal is detected and then goes away: an object tracker is created
        for it. If this object tracker has a long fade out time, and then a
        signal far away from the original is created, no additional object
        tracker will be created: len(candidates) == len(self.object_trackers)
        until the first object tracker is removed. In practice, this is rarely
        an issue since fade out times are typically short, but it should still
        be addressed in the future, possibly by implementing a priority queue.
        """

        # If we have more unassigned locations than object trackers,
        # create more object trackers.
        while len(candidates) > len(self.object_trackers):
            object_tracker = ObjectTracker(**self.kwargs)
            self.object_trackers.append(object_tracker)

        for object_tracker in self.object_trackers:
            detected_location = object_tracker.update_detected_location(candidates)

            # If a candidate location was picked, remove it so another tracked
            # object doesn't try to also assign itself to that location, and
            # remove all other candidate locations within the exclusion radius
            # of the detected location.
            if detected_location is not None:
                candidates.remove(detected_location)
                candidates = [
                    c
                    for c in candidates
                    if c.distance_to(detected_location) > self.exclusion_radius
                ]

            # If a candidate location wasn't picked and the tracker has faded
            # out, remove it so we don't keep processing over it.
            elif object_tracker.fadeout_progress() > 1.0:
                self.object_trackers.remove(object_tracker)

    def update_current_locations(self):
        for object_tracker in self.object_trackers:
            object_tracker.update_current_location()

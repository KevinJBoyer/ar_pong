from math import sqrt
import time
from typing import Optional
from . import Distance, Point, closest_to, dist, interpolate

# todo: add tests
class DetectedObject:
    # The last location we detected the object at.
    # This comes from some (noisy) signal, like MediaPipe.
    last_detected_location: Optional[Point] = None

    # The location we currently report the object at.
    # We calculate this based on the noisy signal, and want to report a smooth
    # value that reduces or eliminates the noise from the signal
    current_location: Optional[Point] = None

    # The last time we detected a location from the object.
    last_detection_time: Optional[float] = None

    # How fast the current location "catches up" to the detected location.
    interpolation_speed: float = 0.7

    # Number of seconds without detection before we reset current_location.
    # Set to None for no fadeout.
    fadeout_timer: Optional[float] = 2.0

    def fadeout_progress(self) -> float:
        """
        Returns the percentage of the fadeout timer that has elapsed since
        last detection, or 0.0 if there is fadeout_timer is None.
        """

        if self.last_detection_time and self.fadeout_timer:
            return (time.time() - self.last_detection_time) / self.fadeout_timer
        else:
            return 0.0

    def update_detected_location(self, candidates: list[Point]) -> None:
        if len(candidates) == 0:
            return

        self.last_detection_time = time.time()

        # If there's no current location, pick an arbitrary candidate location
        if not self.current_location:
            self.last_detected_location = candidates[0]

        # If there is a current location, pick the closest candidate to it
        else:
            self.last_detected_location = closest_to(self.current_location, candidates)

    def update_current_location(self) -> None:
        # If enough time has passed since we last detected a location, don't
        # report a current location
        if self.fadeout_progress() > 1.0:
            self.current_location = None

        elif self.last_detected_location is not None:
            # we have a last detected location, but no current location
            if self.current_location is None:
                self.current_location = self.last_detected_location

            # we have a last detected location AND a current location
            else:
                self.current_location = interpolate(
                    self.current_location,
                    self.last_detected_location,
                    self.interpolation_speed,
                )

import time
from typing import Optional

from .point import Point


class ObjectTracker:
    def __init__(
        self,
        fadein_threshold=1.0,
        fadeout_threshold=1.0,
        detection_radius=0.5,
        interpolation_speed=0.7,
    ):
        # The last location we detected the object at.
        # This comes from some noisy signal, like MediaPipe.
        self.last_detected_location: Optional[Point] = None

        # The location we currently report the object at.
        # We calculate this based on the noisy signal, and want to report a smooth
        # value that reduces or eliminates the noise from the signal.
        self.current_location: Optional[Point] = None

        # The first and last times we detected a location from the object.
        self.first_detection_time: Optional[float] = None
        self.last_detection_time: Optional[float] = None

        # Number of seconds after detection before we set current_location.
        # Set to None (or 0.0) to immediately report current location.
        self.fadein_threshold: Optional[float] = fadein_threshold

        # Number of seconds without detection before we reset current_location.
        # Set to None for continue reporting current location indefinitely.
        self.fadeout_threshold: Optional[float] = fadeout_threshold

        # We ignore candidate detected locations that are further away from our
        # current location than this distance.
        self.detection_radius: Optional[float] = detection_radius

        # How fast the current location "catches up" to the detected location.
        # Set to 1.0 for no interpolation.
        self.interpolation_speed: float = interpolation_speed

    def _filter_by_detection_radius(self, candidates: list[Point]) -> list[Point]:
        if self.detection_radius is not None and self.current_location is not None:
            return [
                c
                for c in candidates
                if c.distance_to(self.current_location) < self.detection_radius
            ]
        return candidates

    def _timer_percentange(
        self, start_time: Optional[float], threshold: Optional[float]
    ) -> Optional[float]:
        """Returns time since benchmark as a percentage of threshold."""

        if start_time and threshold:
            return (time.time() - start_time) / threshold

        return None

    def fadein_progress(self) -> float:
        """
        Returns the percentage of the fadeout timer that has elapsed since
        last detection, or 1.0 if fadeout_timer is None.
        """

        percentage = self._timer_percentange(
            self.first_detection_time, self.fadein_threshold
        )
        return percentage if percentage is not None else 1.0

    def fadeout_progress(self) -> float:
        """
        Returns the percentage of the fadeout timer that has elapsed since
        last detection, or 0.0 if is fadeout_timer is None.
        """

        percentage = self._timer_percentange(
            self.last_detection_time, self.fadeout_threshold
        )
        return percentage if percentage is not None else 1.0

    def update_detected_location(self, candidates: list[Point]) -> Optional[Point]:
        """Return the new detected_location, or None if not updated."""

        nearby_candidates = self._filter_by_detection_radius(candidates)

        if len(nearby_candidates) == 0:
            return None

        if self.first_detection_time is None:
            self.first_detection_time = time.time()

        self.last_detection_time = time.time()

        # If there's no current location, pick an arbitrary candidate location
        if not self.current_location:
            self.last_detected_location = nearby_candidates[0]

        # If there is a current location, pick the closest candidate to it
        else:
            self.last_detected_location = self.current_location.closest_to(
                nearby_candidates
            )

        return self.last_detected_location

    def update_current_location(self) -> None:
        # If we haven't yet faded in, or we have already faded out
        if self.fadein_progress() < 1.0 or self.fadeout_progress() > 1.0:
            self.current_location = None

        elif self.last_detected_location is not None:
            # We have a last detected location, but no current location
            if self.current_location is None:
                self.current_location = self.last_detected_location

            # We have a last detected location AND a current location
            else:
                self.current_location = self.current_location.interpolate_toward(
                    self.last_detected_location,
                    speed=self.interpolation_speed,
                )

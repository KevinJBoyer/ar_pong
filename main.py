import cv2
import time

from handstracker import HandsTracker


def main():
    camera_id = 0
    camera = cv2.VideoCapture(camera_id)

    RUN = True
    success, img = camera.read()
    h, w, c = img.shape
    hands_tracker = HandsTracker()

    while RUN:
        success, img = camera.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        hands_tracker.update(imgRGB)
        hands_tracker.draw(img)

        for hand in hands_tracker.tracked_hands.object_trackers:
            if hand.current_location is not None:
                x = hand.current_location.x
                y = hand.current_location.y
                cv2.circle(img, (int(w * x), int(h * y)), 25, (0, 255, 255), cv2.FILLED)

        cv2.imshow("Image", img)

        keypress = cv2.waitKey(1)
        if keypress == 27:  # Escape key
            RUN = False


if __name__ == "__main__":
    main()

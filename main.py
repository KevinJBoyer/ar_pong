import cv2
import time

from mediapipeui.handtracker import HandTracker

cap = cv2.VideoCapture(0)

pTime = 0.0
cTime = 0.0

RUN = True
success, img = cap.read()
h, w, c = img.shape
hands_tracker = HandTracker()

while RUN:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    hands_tracker.update(imgRGB)
    hands_tracker.draw(img)

    if hands_tracker.hand.current_location is not None:
        x = hands_tracker.hand.current_location.x
        y = hands_tracker.hand.current_location.y
        cv2.circle(img, (int(w * x), int(h * y)), 25, (0, 255, 255), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(
        img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3
    )

    cv2.imshow("Image", img)

    keypress = cv2.waitKey(1)
    if keypress == 27:  # Escape key
        RUN = False

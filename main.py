import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

hands = mp.solutions.hands.Hands(
    static_image_mode=False,
    model_complexity = 0
)

mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

RUN = True

pong_x = .5
pong_y = .5

HIT_THRESHOLD = 0.05

speed = 0.007
x_d = 1
y_d = 1

success, img = cap.read()
h, w, c = img.shape

HIT_DELAY = 25
hit_delay_counter = 0

while RUN:
    hit_delay_counter += 1 if hit_delay_counter < HIT_DELAY else 0
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:
            
            x = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].x
            y = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].y

            cv2.circle(img, (int(w * x), int(h * y)), 25, (0,255,255), cv2.FILLED)

            if abs(x - pong_x) < HIT_THRESHOLD and abs(y - pong_y) < HIT_THRESHOLD and hit_delay_counter == HIT_DELAY:
                print("HIT")
                x_d *= -1
                hit_delay_counter = 0

            #mpDraw.draw_landmarks(
            #    img, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS
            #)

    # update ball location
    pong_x += speed * x_d
    pong_y += speed * y_d


    if pong_x > 1.0 or pong_x < 0.0:
        RUN=False
    
    if pong_y > 1.0:
        pong_y = 1.0
        y_d = -1
    elif pong_y < 0.0:
        pong_y = 0.0
        y_d = 1

    # draw it
    cv2.circle(img, (int(w * pong_x), int(h * pong_y)), 25, (255,0,255), cv2.FILLED)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(
        img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3
    )

    cv2.imshow("Image", img)

    keypress = cv2.waitKey(1)
    if keypress == 27: # Escape key
        RUN = False
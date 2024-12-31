import cv2
import mediapipe as mp
import pyautogui
import math


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

screen_width, screen_height = pyautogui.size()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

  
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
         
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark

            index_finger_tip = landmarks[8]
            thumb_tip = landmarks[4]

       
            x = int(index_finger_tip.x * frame_width)
            y = int(index_finger_tip.y * frame_height)
            screen_x = int(index_finger_tip.x * screen_width)
            screen_y = int(index_finger_tip.y * screen_height)

            pyautogui.moveTo(screen_x, screen_y)

            # Calculate the distance between the index finger tip and the thumb tip
            thumb_x = int(thumb_tip.x * frame_width)
            thumb_y = int(thumb_tip.y * frame_height)
            distance = math.hypot(thumb_x - x, thumb_y - y)

           
            if distance < 40:  # Adjust threshold for sensitivity
                pyautogui.click()

    # Display the webcam feed with landmarks
    cv2.imshow('Virtual Mouse with Click', frame)

    # Break the loop if 'Esc' is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()

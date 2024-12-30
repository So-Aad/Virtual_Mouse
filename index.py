import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize MediaPipe Hands and PyAutoGUI
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

screen_width, screen_height = pyautogui.size()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    # Convert the frame to RGB for processing with MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw the hand landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark

            # Extract the tip of the index finger (landmark 8) and the tip of the thumb (landmark 4)
            index_finger_tip = landmarks[8]
            thumb_tip = landmarks[4]

            # Convert finger tip positions to screen coordinates
            x = int(index_finger_tip.x * frame_width)
            y = int(index_finger_tip.y * frame_height)
            screen_x = int(index_finger_tip.x * screen_width)
            screen_y = int(index_finger_tip.y * screen_height)

            # Move the mouse cursor to the new position
            pyautogui.moveTo(screen_x, screen_y)

            # Calculate the distance between the index finger tip and the thumb tip
            thumb_x = int(thumb_tip.x * frame_width)
            thumb_y = int(thumb_tip.y * frame_height)
            distance = math.hypot(thumb_x - x, thumb_y - y)

            # If the distance is small enough, simulate a mouse click (pinch gesture)
            if distance < 40:  # Adjust threshold for sensitivity
                pyautogui.click()

    # Display the webcam feed with landmarks
    cv2.imshow('Virtual Mouse with Click', frame)

    # Break the loop if 'Esc' is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

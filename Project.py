# Import necessary libraries
import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
import random

# Initialize webcam capture
cap = cv2.VideoCapture(0)

# Initialize hand detector with max 1 hand detection
detector = HandDetector(maxHands=1)

# Set webcam resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1020)

# Initialize game state variables
timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # scores[0] = AI, scores[1] = Player

# Debug: Print camera dimensions
print("Width:", cap.get(3))
print("Height:", cap.get(4))

# Placeholder for AI image (rock, paper, or scissors)
imageAi = None

# Main loop
while True:
    # Load background image
    imgbg = cv2.imread('resources/BG.png')

    # Read frame from webcam
    success, img = cap.read()

    # Resize and flip webcam image
    imgscaled = cv2.resize(img, (0, 0), None, 0.23, 0.32)
    imgscaled = cv2.flip(imgscaled, 1)
    img = cv2.flip(img, 1)

    # Detect hands in the scaled image
    hands, img = detector.findHands(imgscaled)

    # If game has started
    if startGame:
        # If result is not yet shown, start timer
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgbg, str(int(timer)), (600, 435),
                        cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            # After 3 seconds, evaluate the result
            if timer > 3:
                stateResult = True
                timer = 0

                # Check if hand is detected
                if hands:
                    hand = hands[0]
                    playermove = 0

                    # Detect gesture using finger positions
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playermove = 1  # Rock
                    if fingers == [1, 1, 1, 1, 1]:
                        playermove = 2  # Paper
                    if fingers == [0, 1, 1, 0, 0]:
                        playermove = 3  # Scissors

                    # Generate AI's move randomly
                    randomno = random.randint(1, 3)
                    imageAi = cv2.imread(f"resources/{randomno}.png", cv2.IMREAD_UNCHANGED)

                    # Overlay AI move on background
                    imgbg = cvzone.overlayPNG(imgbg, imageAi, (149, 310))

                    # Update scores based on outcome
                    if playermove != 0:
                        if (playermove == 1 and randomno == 3) or \
                           (playermove == 2 and randomno == 1) or \
                           (playermove == 3 and randomno == 2):
                            scores[1] += 1  # Player wins
                        elif (playermove == 3 and randomno == 1) or \
                             (playermove == 1 and randomno == 2) or \
                             (playermove == 2 and randomno == 3):
                            scores[0] += 1  # AI wins
                    else:
                        # No recognizable hand gesture
                        cv2.putText(imgbg, "No hand detected!", (450, 500),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 4)
                        time.sleep(2)
                        imageAi = None

    # Show result image if available
    if stateResult and imageAi is not None:
        imgbg = cvzone.overlayPNG(imgbg, imageAi, (149, 310))

    # Display scores
    cv2.putText(imgbg, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgbg, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    # Show webcam feed on background
    imgbg[233:658, 795:1200] = imgscaled

    # Display start prompt if game hasn't started
    if not startGame:
        cv2.putText(imgbg, "Press 'S' to Start", (480, 650),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 4)

    # Show final frame
    cv2.imshow("imgbg", imgbg)

    # Listen for keyboard input
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        print("Game started")
        stateResult = False
    elif key == ord('q'):
        print("Game exited")
        break

# Release camera and close window
cap.release()
cv2.destroyAllWindows()

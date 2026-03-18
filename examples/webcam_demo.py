"""
Minimal webcam demo — runs gesture detection + classification in a loop
and prints results to stdout. No server needed.

    python examples/webcam_demo.py
"""

import cv2
from ai_engine.gesture_detector import detect_hands, create_detector
from ai_engine.gesture_classifier import classify_gesture

cap = cv2.VideoCapture(0)
detector = create_detector(max_hands=2)

print("press q to quit")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    for hand in detect_hands(frame, detector):
        result = classify_gesture(hand.landmarks)
        print(f"  {hand.handedness}: {result['gesture']} ({result['confidence']:.0%})")

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()

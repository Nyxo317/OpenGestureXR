"""
Classify a single image file instead of a live webcam feed.

    python examples/classify_image.py path/to/hand.jpg
"""

import sys
import cv2
from ai_engine.gesture_detector import detect_hands, create_detector
from ai_engine.gesture_classifier import classify_gesture

if len(sys.argv) < 2:
    print("usage: python examples/classify_image.py <image_path>")
    sys.exit(1)

frame = cv2.imread(sys.argv[1])
if frame is None:
    print(f"could not read {sys.argv[1]}")
    sys.exit(1)

for hand in detect_hands(frame, create_detector(max_hands=2)):
    result = classify_gesture(hand.landmarks)
    print(f"{hand.handedness}: {result['gesture']} ({result['confidence']:.0%})")

import cv2
import mediapipe as mp
import numpy as np
import time
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands =  mp_hands.Hands(min_detection_confidence=0.7)
col1 = (255,0,0)
col2 = (0,255,0)
thk = 2
fng_tips = [4,8,12,16,20]
radius = 6

def detect_hands(img, draw=False):
    detect_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(detect_img)
    h, w, c = img.shape
    lbh = []
    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            locations = {}
            lbh.append(locations)
            for id, lm in enumerate(hand_lms.landmark):
                x, y, z = int(lm.x*w), int(lm.y*h), lm.z
                locations[id] = (x,y,z)
            if draw:
                mp_drawing.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
    return lbh

def get_landmark_distance(locations, lm_id1, lm_id2, img=None, draw=False):
    if not lm_id1 in locations or not lm_id2 in locations:
        return None
    (x1,y1,z1) = locations[lm_id1]
    (x2,y2,z2) = locations[lm_id2]
    return get_distance((x1,y1), (x2,y2), img=img, draw=draw)

def get_distance(p1, p2, img=None, draw=False):
    (x1,y1) = p1
    (x2,y2) = p2
    if x1 and y1 and x2 and y2:
        if not img is None and draw:
            cv2.circle(img, (x1,y1), radius, col2, thickness=thk)
            cv2.circle(img, (x2,y2), radius, col2, thickness=thk)
            cv2.line(img, (x1,y1), (x2,y2), col1, thickness=thk)
        return math.hypot(x1-x2, y1-y2)
    return None

def get_finger_tip_centroid(locations, img=None, draw=False):
    for id in fng_tips:
        if not id in locations:
            return None
    x_all = []
    y_all = []
    for id in fng_tips:
        (x,y,z) = locations[id]
        x_all.append(x)
        y_all.append(y)
    x_mean = int(np.mean(x_all))
    y_mean = int(np.mean(y_all))
    if not img is None and draw:
        for x,y in zip(x_all, y_all):
            cv2.line(img, (x,y), (x_mean,y_mean), col1, thickness=thk)
            cv2.circle(img, (x,y), radius, col2, thickness=thk)
        cv2.circle(img, (x_mean,y_mean), radius, col2, thickness=thk)
    return (x_mean, y_mean)

def full_detect_hands(img, draw=False, skip=False):
    if skip:
        return img
    lbh = detect_hands(img, draw=True)
    for locations in lbh:
        d1 = get_landmark_distance(locations, 4, 8, img=img, draw=draw)
        d2 = get_landmark_distance(locations, 12, 8, img=img, draw=draw)
        d3 = get_landmark_distance(locations, 12, 16, img=img, draw=draw)
        d4 = get_landmark_distance(locations, 16, 20, img=img, draw=draw)
        d5 = get_landmark_distance(locations, 4, 20, img=img, draw=draw)
        fng_centroid = get_finger_tip_centroid(locations, img=img, draw=draw)
    return img
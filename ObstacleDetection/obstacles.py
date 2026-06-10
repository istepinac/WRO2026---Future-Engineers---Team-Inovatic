import cv2
import numpy as np
import math

# -----------------------
# SETTINGS
# -----------------------
FRAME_W = 320
FRAME_H = 240

BASE_SPEED = 0.5
TURN_GAIN = 0.7

Kp = 0.004
Kd = 0.002

OFFSET = 80

# State machine
STATE_DRIVE = "DRIVE"
STATE_AVOID_LEFT = "AVOID_LEFT"
STATE_AVOID_RIGHT = "AVOID_RIGHT"
STATE_RETURN = "RETURN"

state = STATE_DRIVE

# Timers
avoid_timer = 0
return_timer = 0

# Detection stability counters
GREEN_COUNT = 0
RED_COUNT = 0

# PID memory
last_error = 0

# -----------------------
# CAMERA
# -----------------------
cap = cv2.VideoCapture(0)
cap.set(3, FRAME_W)
cap.set(4, FRAME_H)

# -----------------------
# HELPER FUNCTIONS
# -----------------------
def find_rectangle(mask):
    best_area = 0
    best_rect = None

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        area = cv2.contourArea(c)
        if area > 1500:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)

            if len(approx) == 4:
                x,y,w,h = cv2.boundingRect(approx)
                if area > best_area:
                    best_area = area
                    best_rect = (x,y,w,h)

    return best_rect, best_area


def detect_colors(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Morphology kernel
    kernel = np.ones((5,5), np.uint8)

    # GREEN
    lower_g = np.array([40,40,40])
    upper_g = np.array([80,255,255])
    mask_g = cv2.inRange(hsv, lower_g, upper_g)
    mask_g = cv2.morphologyEx(mask_g, cv2.MORPH_OPEN, kernel)
    mask_g = cv2.morphologyEx(mask_g, cv2.MORPH_CLOSE, kernel)

    # RED
    lower_r1 = np.array([0,120,70])
    upper_r1 = np.array([10,255,255])
    lower_r2 = np.array([170,120,70])
    upper_r2 = np.array([180,255,255])
    mask_r = cv2.inRange(hsv, lower_r1, upper_r1) + \
             cv2.inRange(hsv, lower_r2, upper_r2)
    mask_r = cv2.morphologyEx(mask_r, cv2.MORPH_OPEN, kernel)
    mask_r = cv2.morphologyEx(mask_r, cv2.MORPH_CLOSE, kernel)

    g_rect, g_area = find_rectangle(mask_g)
    r_rect, r_area = find_rectangle(mask_r)

    result = {
        "green": {"seen": False, "cx": None, "area": 0, "rect": None},
        "red":   {"seen": False, "cx": None, "area": 0, "rect": None}
    }

    if g_rect:
        x,y,w,h = g_rect
        result["green"]["seen"] = True
        result["green"]["cx"] = x + w//2
        result["green"]["area"] = g_area
        result["green"]["rect"] = g_rect

    if r_rect:
        x,y,w,h = r_rect
        result["red"]["seen"] = True
        result["red"]["cx"] = x + w//2
        result["red"]["area"] = r_area
        result["red"]["rect"] = r_rect

    return result


def pid_control(error):
    global last_error

    derivative = error - last_error
    output = Kp * error + Kd * derivative

    last_error = error
    return output


def clamp(val, min_v, max_v):
    return max(min_v, min(max_v, val))


# -----------------------
# MAIN LOOP
# -----------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (FRAME_W, FRAME_H))
    frame = cv2.GaussianBlur(frame, (5,5), 0)

    detections = detect_colors(frame)

    green_seen = detections["green"]["seen"]
    red_seen = detections["red"]["seen"]

    # STABILITY FILTER
    if green_seen:
        GREEN_COUNT += 1
    else:
        GREEN_COUNT -= 1

    if red_seen:
        RED_COUNT += 1
    else:
        RED_COUNT -= 1

    GREEN_COUNT = clamp(GREEN_COUNT, 0, 5)
    RED_COUNT = clamp(RED_COUNT, 0, 5)

    green_valid = GREEN_COUNT >= 3
    red_valid = RED_COUNT >= 3

    frame_center = FRAME_W // 2

    steering = 0

    # STATE MACHINE
    if state == STATE_DRIVE:

        # default: go straight
        error = 0
        steering = pid_control(error)

        if green_valid:
            state = STATE_AVOID_LEFT
            avoid_timer = 0

        elif red_valid:
            state = STATE_AVOID_RIGHT
            avoid_timer = 0


    elif state == STATE_AVOID_LEFT:

        cx = detections["green"]["cx"] if detections["green"]["cx"] else frame_center
        error = (cx - frame_center) - OFFSET
        steering = pid_control(error)

        avoid_timer += 1

        if avoid_timer > 20:
            state = STATE_RETURN
            return_timer = 0


    elif state == STATE_AVOID_RIGHT:

        cx = detections["red"]["cx"] if detections["red"]["cx"] else frame_center
        error = (cx - frame_center) + OFFSET
        steering = pid_control(error)

        avoid_timer += 1

        if avoid_timer > 20:
            state = STATE_RETURN
            return_timer = 0


    elif state == STATE_RETURN:

        error = 0
        steering = pid_control(error)

        return_timer += 1

        if return_timer > 15:
            state = STATE_DRIVE


    # MOTOR OUTPUT (SIMULATED)
    steering = clamp(steering, -1, 1)

    left_motor = BASE_SPEED - steering * TURN_GAIN
    right_motor = BASE_SPEED + steering * TURN_GAIN

    # DRAW DEBUG
    if detections["green"]["rect"]:
        x,y,w,h = detections["green"]["rect"]
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    if detections["red"]["rect"]:
        x,y,w,h = detections["red"]["rect"]
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)

    cv2.putText(frame, f"State: {state}", (10,20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    cv2.putText(frame, f"L:{left_motor:.2f} R:{right_motor:.2f}", (10,45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
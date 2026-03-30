import cv2
import mediapipe as mp
import pyautogui
import pygetwindow as gw
import time
from collections import deque

# =========================
# SETTINGS
# =========================
CAMERA_INDEX = 0
FRAME_WIDTH = 960
FRAME_HEIGHT = 720

# False = hand up -> page down, hand down -> page up
# True = reverse
REVERSE_SCROLL = False

MOVEMENT_THRESHOLD = 0.006
SCROLL_MULTIPLIER = 3000
SMOOTHING_FRAMES = 7
SCROLL_COOLDOWN = 0.05

BROWSER_KEYWORDS = ["chrome", "edge", "firefox", "brave", "opera"]

pyautogui.FAILSAFE = False

# =========================
# MEDIAPIPE
# =========================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# =========================
# CAMERA
# =========================
cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

# =========================
# STATE
# =========================
prev_y = None
movement_buffer = deque(maxlen=SMOOTHING_FRAMES)
last_scroll_time = 0


# =========================
# HELPERS
# =========================
def is_browser_active():
    try:
        win = gw.getActiveWindow()
        if not win or not win.title:
            return False
        title = win.title.lower()
        return any(keyword in title for keyword in BROWSER_KEYWORDS)
    except Exception:
        return False


def finger_up(landmarks, tip_idx, pip_idx):
    return landmarks[tip_idx].y < landmarks[pip_idx].y


def get_finger_states(landmarks):
    index_up = finger_up(landmarks, 8, 6)
    middle_up = finger_up(landmarks, 12, 10)
    ring_up = finger_up(landmarks, 16, 14)
    pinky_up = finger_up(landmarks, 20, 18)

    return {
        "index": index_up,
        "middle": middle_up,
        "ring": ring_up,
        "pinky": pinky_up
    }


def is_index_only(states):
    return (
        states["index"]
        and not states["middle"]
        and not states["ring"]
        and not states["pinky"]
    )


def draw_text(frame, text, y, color=(255, 255, 255)):
    cv2.putText(
        frame,
        text,
        (20, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        color,
        2
    )


# =========================
# MAIN LOOP
# =========================
print("Program started.")
print("Raise only one finger (index finger).")
print("Move hand up/down to scroll browser.")
print("Press Q to quit.")

while True:
    success, frame = cap.read()
    if not success:
        print("Camera not working.")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    h, w, _ = frame.shape
    browser_active = is_browser_active()
    status_text = "Show one finger"
    mode_text = "Waiting"

    if result.multi_hand_landmarks:
        hand_landmarks_obj = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_landmarks_obj, mp_hands.HAND_CONNECTIONS)

        landmarks = hand_landmarks_obj.landmark
        states = get_finger_states(landmarks)

        if is_index_only(states):
            mode_text = "One finger detected"

            index_tip = landmarks[8]
            x_px = int(index_tip.x * w)
            y_px = int(index_tip.y * h)
            cv2.circle(frame, (x_px, y_px), 10, (0, 255, 0), -1)

            current_y = index_tip.y

            if browser_active:
                if prev_y is not None:
                    dy = current_y - prev_y
                    movement_buffer.append(dy)

                    avg_dy = sum(movement_buffer) / len(movement_buffer)
                    now = time.time()

                    if abs(avg_dy) > MOVEMENT_THRESHOLD and (now - last_scroll_time) > SCROLL_COOLDOWN:
                        scroll_amount = int(-avg_dy * SCROLL_MULTIPLIER)

                        if REVERSE_SCROLL:
                            scroll_amount = -scroll_amount

                        if scroll_amount > 0:
                            scroll_amount = max(scroll_amount, 40)
                        else:
                            scroll_amount = min(scroll_amount, -40)

                        pyautogui.scroll(scroll_amount)
                        last_scroll_time = now

                        if scroll_amount > 0:
                            status_text = f"Scrolling UP page ({scroll_amount})"
                        else:
                            status_text = f"Scrolling DOWN page ({scroll_amount})"

                prev_y = current_y
            else:
                prev_y = None
                movement_buffer.clear()
                status_text = "Browser not active"
        else:
            prev_y = None
            movement_buffer.clear()
            mode_text = "Raise only index finger"
    else:
        prev_y = None
        movement_buffer.clear()
        mode_text = "No hand detected"

    draw_text(
        frame,
        f"Browser Active: {browser_active}",
        30,
        (0, 255, 0) if browser_active else (0, 0, 255)
    )
    draw_text(frame, mode_text, 60, (255, 255, 255))
    draw_text(frame, status_text, 90, (0, 200, 255))
    draw_text(frame, "Only index finger = scroll", FRAME_HEIGHT - 30)

    cv2.imshow("Hand Browser Scroll", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
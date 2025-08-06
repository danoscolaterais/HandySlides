import cv2
import mediapipe as mp
import pyautogui
import time

last_press_time = 0
cooldown_period = 1

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Webcam does not work")
    exit()

def is_arm_raised(landmarks):
    if not landmarks:
        return None
        
    left_shoulder = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_wrist = landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
    right_wrist = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]

    print(f"L.Shoulder.y: {left_shoulder.y:.3f}, L.Wrist.y: {left_wrist.y:.3f}")
    print(f"R.Shoulder.y: {right_shoulder.y:.3f}, R.Wrist.y: {right_wrist.y:.3f}")

    if left_wrist.y < left_shoulder.y - 0.05:
        return "Left"

    if right_wrist.y < right_shoulder.y - 0.05:
        return "Right"

    return None

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error capturng frame.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            raised_arm = is_arm_raised(results.pose_landmarks)
            current_time = time.time()
            
            if raised_arm == "Right" and (current_time - last_press_time > cooldown_period):
                print("Right arm raised!")
                pyautogui.press("up")
                last_press_time = current_time
                
            elif raised_arm == "Left" and (current_time - last_press_time > cooldown_period):
                print("Left arm raised!")
                pyautogui.press("down")
                last_press_time = current_time

        else:
            print("Pose not detected.")
        
        cv2.imshow("Arm Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

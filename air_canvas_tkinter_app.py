import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
import mediapipe as mp
from collections import deque

# Drawing setup
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]
blue_index = green_index = red_index = yellow_index = 0
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# Persistent canvas (black background)
paintWindow = np.zeros((471, 636, 3), dtype=np.uint8)

# Mediapipe hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.9)
mpDraw = mp.solutions.drawing_utils

# Tkinter GUI setup
root = tk.Tk()
root.title("Air Canvas - Tkinter GUI")

# Two panels: left for webcam, right for canvas
video_panel = tk.Label(root)
video_panel.pack(side="left")
canvas_panel = tk.Label(root)
canvas_panel.pack(side="right")

cap = cv2.VideoCapture(0)

def update():
    global bpoints, gpoints, rpoints, ypoints
    global blue_index, green_index, red_index, yellow_index, colorIndex
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape

        # Draw color buttons on frame
        cv2.rectangle(frame, (40, 1), (140, 65), (255, 255, 255), 2)
        cv2.rectangle(frame, (160, 1), (255, 65), (255, 0, 0), 2)
        cv2.rectangle(frame, (275, 1), (370, 65), (0, 255, 0), 2)
        cv2.rectangle(frame, (390, 1), (485, 65), (0, 0, 255), 2)
        cv2.rectangle(frame, (505, 1), (600, 65), (0, 255, 255), 2)
        cv2.rectangle(frame, (160, 1), (255, 65), (255, 0, 0), -1)
        cv2.rectangle(frame, (275, 1), (370, 65), (0, 255, 0), -1)
        cv2.rectangle(frame, (390, 1), (485, 65), (0, 0, 255), -1)
        cv2.rectangle(frame, (505, 1), (600, 65), (0, 255, 255), -1)
        cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(framergb)

        if result.multi_hand_landmarks:
            for handslms in result.multi_hand_landmarks:
                landmarks = []
                for lm in handslms.landmark:
                    lmx = int(lm.x * w)
                    lmy = int(lm.y * h)
                    landmarks.append([lmx, lmy])
                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                if len(landmarks) >= 9:
                    fore_finger = (landmarks[8][0], landmarks[8][1])
                    center = fore_finger
                    thumb = (landmarks[4][0], landmarks[4][1])

                    if (thumb[1] - center[1] < 30):
                        bpoints.append(deque(maxlen=512))
                        blue_index += 1
                        gpoints.append(deque(maxlen=512))
                        green_index += 1
                        rpoints.append(deque(maxlen=512))
                        red_index += 1
                        ypoints.append(deque(maxlen=512))
                        yellow_index += 1

                    elif center[1] <= 65:
                        if 40 <= center[0] <= 140:  # Clear Button
                            bpoints = [deque(maxlen=1024)]
                            gpoints = [deque(maxlen=1024)]
                            rpoints = [deque(maxlen=1024)]
                            ypoints = [deque(maxlen=1024)]
                            blue_index = green_index = red_index = yellow_index = 0
                            paintWindow[67:, :, :] = 0  # black
                        elif 160 <= center[0] <= 255:
                            colorIndex = 0  # Blue
                        elif 275 <= center[0] <= 370:
                            colorIndex = 1  # Green
                        elif 390 <= center[0] <= 485:
                            colorIndex = 2  # Red
                        elif 505 <= center[0] <= 600:
                            colorIndex = 3  # Yellow
                    else:
                        if colorIndex == 0:
                            bpoints[blue_index].appendleft(center)
                        elif colorIndex == 1:
                            gpoints[green_index].appendleft(center)
                        elif colorIndex == 2:
                            rpoints[red_index].appendleft(center)
                        elif colorIndex == 3:
                            ypoints[yellow_index].appendleft(center)
        else:
            bpoints.append(deque(maxlen=512))
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1

        # Draw lines of all the colors on the canvas and frame
        points = [bpoints, gpoints, rpoints, ypoints]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                    cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

        # Show webcam with drawing overlay
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_panel.imgtk = imgtk
        video_panel.configure(image=imgtk)

        # Show persistent canvas
        canvas_img = Image.fromarray(paintWindow)
        canvas_imgtk = ImageTk.PhotoImage(image=canvas_img)
        canvas_panel.imgtk = canvas_imgtk
        canvas_panel.configure(image=canvas_imgtk)

    root.after(10, update)

update()
root.mainloop()
cap.release()
cv2.destroyAllWindows()

# import tkinter as tk
# from PIL import Image, ImageTk
# import cv2
# import numpy as np
# import mediapipe as mp
# from collections import deque

# # Drawing setup
# bpoints = [deque(maxlen=1024)]
# gpoints = [deque(maxlen=1024)]
# rpoints = [deque(maxlen=1024)]
# ypoints = [deque(maxlen=1024)]
# blue_index = green_index = red_index = yellow_index = 0
# colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
# colorIndex = 0

# # Persistent canvas (black background)
# paintWindow = np.zeros((471, 636, 3), dtype=np.uint8)

# # Mediapipe hands
# mpHands = mp.solutions.hands
# hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.9)
# mpDraw = mp.solutions.drawing_utils

# # Tkinter GUI setup
# root = tk.Tk()
# root.title("Air Canvas - Tkinter GUI")

# # Two panels: left for webcam, right for canvas
# video_panel = tk.Label(root)
# video_panel.pack(side="left")
# canvas_panel = tk.Label(root)
# canvas_panel.pack(side="right")

# cap = cv2.VideoCapture(0)

# def update():
#     global bpoints, gpoints, rpoints, ypoints
#     global blue_index, green_index, red_index, yellow_index, colorIndex
#     ret, frame = cap.read()
#     if ret:
#         frame = cv2.flip(frame, 1)
#         h, w, c = frame.shape

#         # Draw color buttons on frame
#         cv2.rectangle(frame, (40, 1), (140, 65), (255, 255, 255), 2)
#         cv2.rectangle(frame, (160, 1), (255, 65), (255, 0, 0), 2)
#         cv2.rectangle(frame, (275, 1), (370, 65), (0, 255, 0), 2)
#         cv2.rectangle(frame, (390, 1), (485, 65), (0, 0, 255), 2)
#         cv2.rectangle(frame, (505, 1), (600, 65), (0, 255, 255), 2)
#         cv2.rectangle(frame, (160, 1), (255, 65), (255, 0, 0), -1)
#         cv2.rectangle(frame, (275, 1), (370, 65), (0, 255, 0), -1)
#         cv2.rectangle(frame, (390, 1), (485, 65), (0, 0, 255), -1)
#         cv2.rectangle(frame, (505, 1), (600, 65), (0, 255, 255), -1)
#         cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
#         cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
#         cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
#         cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
#         cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

#         framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         result = hands.process(framergb)

#         if result.multi_hand_landmarks:
#             for handslms in result.multi_hand_landmarks:
#                 landmarks = []
#                 for lm in handslms.landmark:
#                     lmx = int(lm.x * w)
#                     lmy = int(lm.y * h)
#                     landmarks.append([lmx, lmy])
#                 mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

#                 if len(landmarks) >= 9:
#                     fore_finger = (landmarks[8][0], landmarks[8][1])
#                     center = fore_finger
#                     thumb = (landmarks[4][0], landmarks[4][1])

#                     if (thumb[1] - center[1] < 30):
#                         bpoints.append(deque(maxlen=512))
#                         blue_index += 1
#                         gpoints.append(deque(maxlen=512))
#                         green_index += 1
#                         rpoints.append(deque(maxlen=512))
#                         red_index += 1
#                         ypoints.append(deque(maxlen=512))
#                         yellow_index += 1

#                     elif center[1] <= 65:
#                         if 40 <= center[0] <= 140:  # Clear Button
#                             bpoints = [deque(maxlen=1024)]
#                             gpoints = [deque(maxlen=1024)]
#                             rpoints = [deque(maxlen=1024)]
#                             ypoints = [deque(maxlen=1024)]
#                             blue_index = green_index = red_index = yellow_index = 0
#                             paintWindow[67:, :, :] = 0  # black
#                         elif 160 <= center[0] <= 255:
#                             colorIndex = 0  # Blue
#                         elif 275 <= center[0] <= 370:
#                             colorIndex = 1  # Green
#                         elif 390 <= center[0] <= 485:
#                             colorIndex = 2  # Red
#                         elif 505 <= center[0] <= 600:
#                             colorIndex = 3  # Yellow
#                     else:
#                         if colorIndex == 0:
#                             bpoints[blue_index].appendleft(center)
#                         elif colorIndex == 1:
#                             gpoints[green_index].appendleft(center)
#                         elif colorIndex == 2:
#                             rpoints[red_index].appendleft(center)
#                         elif colorIndex == 3:
#                             ypoints[yellow_index].appendleft(center)
#         else:
#             bpoints.append(deque(maxlen=512))
#             blue_index += 1
#             gpoints.append(deque(maxlen=512))
#             green_index += 1
#             rpoints.append(deque(maxlen=512))
#             red_index += 1
#             ypoints.append(deque(maxlen=512))
#             yellow_index += 1

#         # Draw lines of all the colors on the canvas and frame
#         points = [bpoints, gpoints, rpoints, ypoints]
#         for i in range(len(points)):
#             for j in range(len(points[i])):
#                 for k in range(1, len(points[i][j])):
#                     if points[i][j][k - 1] is None or points[i][j][k] is None:
#                         continue
#                     cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
#                     cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

#         # Show webcam with drawing overlay
#         # img = Image.fromarray(frame)
#         img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#         imgtk = ImageTk.PhotoImage(image=img)
#         video_panel.imgtk = imgtk
#         video_panel.configure(image=imgtk)

#         # Show persistent canvas
#         # canvas_img = Image.fromarray(paintWindow)
#         canvas_img = Image.fromarray(cv2.cvtColor(paintWindow, cv2.COLOR_BGR2RGB))
#         canvas_imgtk = ImageTk.PhotoImage(image=canvas_img)
#         canvas_panel.imgtk = canvas_imgtk
#         canvas_panel.configure(image=canvas_imgtk)

#     root.after(10, update)

# update()
# root.mainloop()
# cap.release()
# cv2.destroyAllWindows()




# ///////
# import tkinter as tk
# from PIL import Image, ImageTk
# import cv2
# import numpy as np
# import mediapipe as mp
# from collections import deque

# # Drawing setup
# bpoints = [deque(maxlen=1024)]
# gpoints = [deque(maxlen=1024)]
# rpoints = [deque(maxlen=1024)]
# ypoints = [deque(maxlen=1024)]
# blue_index = green_index = red_index = yellow_index = 0
# colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
# colorIndex = 0

# # Persistent canvas (black background)
# paintWindow = np.zeros((471, 636, 3), dtype=np.uint8)

# # Mediapipe hands
# mpHands = mp.solutions.hands
# hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.9)
# mpDraw = mp.solutions.drawing_utils

# # Tkinter GUI setup
# root = tk.Tk()
# root.title("Air Canvas - Tkinter GUI")

# # Top frame for title and instructions
# top_frame = tk.Frame(root)
# top_frame.pack(side="top", fill="x")
# title = tk.Label(top_frame, text="Air Canvas", font=("Arial", 18, "bold"))
# title.pack(pady=5)
# instructions = tk.Label(top_frame, text="Draw in the air! Use your index finger. Select color below or with gestures.")
# instructions.pack()

# # Middle frame for video and canvas
# middle_frame = tk.Frame(root)
# middle_frame.pack(side="top", fill="both", expand=True)

# video_panel = tk.Label(middle_frame, width=636, height=471)
# video_panel.pack(side="left", padx=10, pady=10)
# canvas_panel = tk.Label(middle_frame, width=636, height=471)
# canvas_panel.pack(side="right", padx=10, pady=10)

# # Bottom frame for color and clear buttons
# bottom_frame = tk.Frame(root)
# bottom_frame.pack(side="bottom", fill="x", pady=10)

# def set_color(idx):
#     global colorIndex
#     colorIndex = idx

# color_names = ["Blue", "Green", "Red", "Yellow"]
# color_values = ["#FF0000", "#00FF00", "#0000FF", "#00FFFF"]
# for i, (name, color) in enumerate(zip(color_names, color_values)):
#     btn = tk.Button(bottom_frame, text=name, bg=color, fg="black", width=10, command=lambda i=i: set_color(i))
#     btn.pack(side="left", padx=5)

# def clear_canvas():
#     global bpoints, gpoints, rpoints, ypoints, blue_index, green_index, red_index, yellow_index, paintWindow
#     bpoints = [deque(maxlen=1024)]
#     gpoints = [deque(maxlen=1024)]
#     rpoints = [deque(maxlen=1024)]
#     ypoints = [deque(maxlen=1024)]
#     blue_index = green_index = red_index = yellow_index = 0
#     paintWindow[67:, :, :] = 0

# clear_btn = tk.Button(bottom_frame, text="Clear Canvas", bg="white", fg="black", width=15, command=clear_canvas)
# clear_btn.pack(side="left", padx=10)

# cap = cv2.VideoCapture(0)

# def update():
#     global bpoints, gpoints, rpoints, ypoints
#     global blue_index, green_index, red_index, yellow_index, colorIndex
#     ret, frame = cap.read()
#     if ret:
#         frame = cv2.flip(frame, 1)
#         h, w, c = frame.shape

#         # Draw color buttons on frame
#         cv2.rectangle(frame, (40, 1), (140, 65), (255, 255, 255), 2)
#         cv2.rectangle(frame, (160, 1), (255, 65), (255, 0, 0), 2)
#         cv2.rectangle(frame, (275, 1), (370, 65), (0, 255, 0), 2)
#         cv2.rectangle(frame, (390, 1), (485, 65), (0, 0, 255), 2)
#         cv2.rectangle(frame, (505, 1), (600, 65), (0, 255, 255), 2)
#         cv2.rectangle(frame, (160, 1), (255, 65), (255, 0, 0), -1)
#         cv2.rectangle(frame, (275, 1), (370, 65), (0, 255, 0), -1)
#         cv2.rectangle(frame, (390, 1), (485, 65), (0, 0, 255), -1)
#         cv2.rectangle(frame, (505, 1), (600, 65), (0, 255, 255), -1)
#         cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
#         cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
#         cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
#         cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
#         cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

#         framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         result = hands.process(framergb)

#         if result.multi_hand_landmarks:
#             for handslms in result.multi_hand_landmarks:
#                 landmarks = []
#                 for lm in handslms.landmark:
#                     lmx = int(lm.x * w)
#                     lmy = int(lm.y * h)
#                     landmarks.append([lmx, lmy])
#                 mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

#                 if len(landmarks) >= 9:
#                     fore_finger = (landmarks[8][0], landmarks[8][1])
#                     center = fore_finger
#                     thumb = (landmarks[4][0], landmarks[4][1])

#                     if (thumb[1] - center[1] < 30):
#                         bpoints.append(deque(maxlen=512))
#                         blue_index += 1
#                         gpoints.append(deque(maxlen=512))
#                         green_index += 1
#                         rpoints.append(deque(maxlen=512))
#                         red_index += 1
#                         ypoints.append(deque(maxlen=512))
#                         yellow_index += 1

#                     elif center[1] <= 65:
#                         if 40 <= center[0] <= 140:  # Clear Button
#                             bpoints = [deque(maxlen=1024)]
#                             gpoints = [deque(maxlen=1024)]
#                             rpoints = [deque(maxlen=1024)]
#                             ypoints = [deque(maxlen=1024)]
#                             blue_index = green_index = red_index = yellow_index = 0
#                             paintWindow[67:, :, :] = 0  # black
#                         elif 160 <= center[0] <= 255:
#                             colorIndex = 0  # Blue
#                         elif 275 <= center[0] <= 370:
#                             colorIndex = 1  # Green
#                         elif 390 <= center[0] <= 485:
#                             colorIndex = 2  # Red
#                         elif 505 <= center[0] <= 600:
#                             colorIndex = 3  # Yellow
#                     else:
#                         if colorIndex == 0:
#                             bpoints[blue_index].appendleft(center)
#                         elif colorIndex == 1:
#                             gpoints[green_index].appendleft(center)
#                         elif colorIndex == 2:
#                             rpoints[red_index].appendleft(center)
#                         elif colorIndex == 3:
#                             ypoints[yellow_index].appendleft(center)
#         else:
#             bpoints.append(deque(maxlen=512))
#             blue_index += 1
#             gpoints.append(deque(maxlen=512))
#             green_index += 1
#             rpoints.append(deque(maxlen=512))
#             red_index += 1
#             ypoints.append(deque(maxlen=512))
#             yellow_index += 1

#         # Draw lines of all the colors on the canvas and frame
#         points = [bpoints, gpoints, rpoints, ypoints]
#         for i in range(len(points)):
#             for j in range(len(points[i])):
#                 for k in range(1, len(points[i][j])):
#                     if points[i][j][k - 1] is None or points[i][j][k] is None:
#                         continue
#                     cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
#                     cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

#         # Show webcam with drawing overlay
#         img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#         imgtk = ImageTk.PhotoImage(image=img)
#         video_panel.imgtk = imgtk
#         video_panel.configure(image=imgtk)

#         # Show persistent canvas
#         canvas_img = Image.fromarray(cv2.cvtColor(paintWindow, cv2.COLOR_BGR2RGB))
#         canvas_imgtk = ImageTk.PhotoImage(image=canvas_img)
#         canvas_panel.imgtk = canvas_imgtk
#         canvas_panel.configure(image=canvas_imgtk)

#     root.after(10, update)

# update()
# root.mainloop()
# cap.release()
# cv2.destroyAllWindows()



# //////
# import tkinter as tk
# from PIL import Image, ImageTk
# import cv2
# import numpy as np
# import mediapipe as mp
# from collections import deque

# # Set desired width and height for each panel
# PANEL_WIDTH = 800
# PANEL_HEIGHT = 600

# # Drawing setup
# bpoints = [deque(maxlen=1024)]
# gpoints = [deque(maxlen=1024)]
# rpoints = [deque(maxlen=1024)]
# ypoints = [deque(maxlen=1024)]
# blue_index = green_index = red_index = yellow_index = 0
# colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
# colorIndex = 0

# # Persistent canvas (black background)
# paintWindow = np.ones((PANEL_HEIGHT, PANEL_WIDTH, 3), dtype=np.uint8) * 255  # White background

# # Mediapipe hands
# mpHands = mp.solutions.hands
# hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.95, 
#                       min_tracking_confidence=0.95) 
# mpDraw = mp.solutions.drawing_utils

# # Tkinter GUI setup
# root = tk.Tk()
# root.title("Air Canvas - Tkinter GUI")
# root.resizable(True, True)
# root.geometry(f"{2*PANEL_WIDTH}x{PANEL_HEIGHT+170}")

# # Top frame for title and instructions
# top_frame = tk.Frame(root)
# top_frame.pack(side="top", fill="x")
# title = tk.Label(top_frame, text="Air Canvas", font=("Arial", 18, "bold"))
# title.pack(pady=5)
# instructions = tk.Label(
#     top_frame,
#     text="Draw in the Air! Use your index finger. Select color below or with gestures. "
#          "Bring your thumb and forefinger close to stop drawing.",
#     font=("Arial", 10)
# )
# instructions.pack()

# # Middle frame for video and canvas, equally divided
# middle_frame = tk.Frame(root)
# middle_frame.pack(side="top", fill="both", expand=True)

# video_panel = tk.Label(middle_frame, width=PANEL_WIDTH, height=PANEL_HEIGHT, bg="white")
# video_panel.pack(side="left", fill="both", expand=True)
# canvas_panel = tk.Label(middle_frame, width=PANEL_WIDTH, height=PANEL_HEIGHT, bg="white")
# canvas_panel.pack(side="right", fill="both", expand=True)

# # Bottom frame for color and clear buttons
# bottom_frame = tk.Frame(root)
# bottom_frame.pack(side="bottom", fill="x", pady=10)

# def set_color(idx):
#     global colorIndex
#     colorIndex = idx

# color_names = ["Blue", "Green", "Red", "Yellow"]
# color_values = ["#0000FF", "#00FF00", "#FF0000", "#FFFF00"]
# for i, (name, color) in enumerate(zip(color_names, color_values)):
#     btn = tk.Button(
#         bottom_frame,
#         text=name,
#         bg=color,
#         fg="black",
#         width=10,
#         font=("Arial", 12, "bold"),
#         command=lambda i=i: set_color(i)
#     )
#     btn.pack(side="left", padx=8, pady=5)

# def clear_canvas():
#     global bpoints, gpoints, rpoints, ypoints, blue_index, green_index, red_index, yellow_index, paintWindow
#     bpoints = [deque(maxlen=1024)]
#     gpoints = [deque(maxlen=1024)]
#     rpoints = [deque(maxlen=1024)]
#     ypoints = [deque(maxlen=1024)]
#     blue_index = green_index = red_index = yellow_index = 0
#     paintWindow[67:, :, :] = 255  # Reset to white background

# clear_btn = tk.Button(
#     bottom_frame,
#     text="Clear Canvas",
#     bg="white",
#     fg="black",
#     width=15,
#     font=("Arial", 12, "bold"),
#     command=clear_canvas
# )
# clear_btn.pack(side="left", padx=15, pady=5)

# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, PANEL_WIDTH)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, PANEL_HEIGHT)

# def update():
#     global bpoints, gpoints, rpoints, ypoints
#     global blue_index, green_index, red_index, yellow_index, colorIndex
#     ret, frame = cap.read()
#     if ret:
#         frame = cv2.flip(frame, 1)
#         frame = cv2.resize(frame, (PANEL_WIDTH, PANEL_HEIGHT))
#         h, w, c = frame.shape

#         # Draw color buttons on frame
#         cv2.rectangle(frame, (40, 1), (140, 65), (128, 128, 128), 2)
#         cv2.rectangle(frame, (160, 1), (255, 65), (255, 0, 0), 2)
#         cv2.rectangle(frame, (275, 1), (370, 65), (0, 255, 0), 2)
#         cv2.rectangle(frame, (390, 1), (485, 65), (0, 0, 255), 2)
#         cv2.rectangle(frame, (505, 1), (600, 65), (0, 255, 255), 2)
#         cv2.rectangle(frame, (160, 1), (255, 65), (255, 0, 0), -1)
#         cv2.rectangle(frame, (275, 1), (370, 65), (0, 255, 0), -1)
#         cv2.rectangle(frame, (390, 1), (485, 65), (0, 0, 255), -1)
#         cv2.rectangle(frame, (505, 1), (600, 65), (0, 255, 255), -1)
#         cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
#         cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
#         cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
#         cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
#         cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)

#         framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         result = hands.process(framergb)

#         if result.multi_hand_landmarks:
#             for handslms in result.multi_hand_landmarks:
#                 landmarks = []
#                 for lm in handslms.landmark:
#                     lmx = int(lm.x * w)
#                     lmy = int(lm.y * h)
#                     landmarks.append([lmx, lmy])
#                 mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

#                 if len(landmarks) >= 9:
#                     fore_finger = (landmarks[8][0], landmarks[8][1])
#                     center = fore_finger
#                     thumb = (landmarks[4][0], landmarks[4][1])

#                     if (thumb[1] - center[1] < 30):
#                         bpoints.append(deque(maxlen=512))
#                         blue_index += 1
#                         gpoints.append(deque(maxlen=512))
#                         green_index += 1
#                         rpoints.append(deque(maxlen=512))
#                         red_index += 1
#                         ypoints.append(deque(maxlen=512))
#                         yellow_index += 1

#                     elif center[1] <= 65:
#                         if 40 <= center[0] <= 140:  # Clear Button
#                             bpoints = [deque(maxlen=1024)]
#                             gpoints = [deque(maxlen=1024)]
#                             rpoints = [deque(maxlen=1024)]
#                             ypoints = [deque(maxlen=1024)]
#                             blue_index = green_index = red_index = yellow_index = 0
#                             paintWindow[67:, :, :] = 255  # black
#                         elif 160 <= center[0] <= 255:
#                             colorIndex = 0  # Blue
#                         elif 275 <= center[0] <= 370:
#                             colorIndex = 1  # Green
#                         elif 390 <= center[0] <= 485:
#                             colorIndex = 2  # Red
#                         elif 505 <= center[0] <= 600:
#                             colorIndex = 3  # Yellow
#                     else:
#                         if colorIndex == 0:
#                             bpoints[blue_index].appendleft(center)
#                         elif colorIndex == 1:
#                             gpoints[green_index].appendleft(center)
#                         elif colorIndex == 2:
#                             rpoints[red_index].appendleft(center)
#                         elif colorIndex == 3:
#                             ypoints[yellow_index].appendleft(center)
#         else:
#             bpoints.append(deque(maxlen=512))
#             blue_index += 1
#             gpoints.append(deque(maxlen=512))
#             green_index += 1
#             rpoints.append(deque(maxlen=512))
#             red_index += 1
#             ypoints.append(deque(maxlen=512))
#             yellow_index += 1

#         # Draw lines of all the colors on the canvas and frame
#         points = [bpoints, gpoints, rpoints, ypoints]
#         for i in range(len(points)):
#             for j in range(len(points[i])):
#                 for k in range(1, len(points[i][j])):
#                     if points[i][j][k - 1] is None or points[i][j][k] is None:
#                         continue
#                     cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
#                     cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

#         # Show webcam with drawing overlay
#         img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#         imgtk = ImageTk.PhotoImage(image=img)
#         video_panel.imgtk = imgtk
#         video_panel.configure(image=imgtk)

#         # Show persistent canvas
#         canvas_img = Image.fromarray(cv2.cvtColor(paintWindow, cv2.COLOR_BGR2RGB))
#         canvas_imgtk = ImageTk.PhotoImage(image=canvas_img)
#         canvas_panel.imgtk = canvas_imgtk
#         canvas_panel.configure(image=canvas_imgtk)

#     root.after(1, update)

# update()
# root.mainloop()
# cap.release()
# cv2.destroyAllWindows()












# //////////

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import mediapipe as mp
from collections import deque

# Set desired width and height for each panel
PANEL_WIDTH = 800
PANEL_HEIGHT = 600

# Drawing setup
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]
blue_index = green_index = red_index = yellow_index = 0
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# Persistent canvas (white background)
paintWindow = np.ones((PANEL_HEIGHT, PANEL_WIDTH, 3), dtype=np.uint8) * 255  # White background

# Mediapipe hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.95, 
                      min_tracking_confidence=0.95) 
mpDraw = mp.solutions.drawing_utils

# Tkinter GUI setup
root = tk.Tk()
root.title("Air Canvas - Tkinter GUI")
root.resizable(True, True)
root.geometry(f"{2*PANEL_WIDTH}x{PANEL_HEIGHT+170}")

# Top frame for title and instructions
top_frame = tk.Frame(root, bg="#f5f5f5")
top_frame.pack(side="top", fill="x")
title = tk.Label(top_frame, text="Air Canvas", font=("Arial", 22, "bold"), bg="#f5f5f5", fg="#222")
title.pack(pady=(10, 0))
instructions = tk.Label(
    top_frame,
    text="Draw in the Air! Use your index finger. Select color below or with gestures. "
         "Bring your thumb and forefinger close to stop drawing.",
    font=("Segoe UI", 11),
    bg="#f5f5f5",
    fg="#444"
)
instructions.pack(pady=(0, 10))

# Middle frame for video and canvas, equally divided
middle_frame = tk.Frame(root, bg="#222")
middle_frame.pack(side="top", fill="both", expand=True, padx=10, pady=5)

video_panel = tk.Label(middle_frame, width=PANEL_WIDTH, height=PANEL_HEIGHT, bg="white", bd=3, relief="ridge")
video_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
canvas_panel = tk.Label(middle_frame, width=PANEL_WIDTH, height=PANEL_HEIGHT, bg="white", bd=3, relief="ridge")
canvas_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))

# Bottom frame for color and clear buttons
bottom_frame = tk.Frame(root, bg="#f5f5f5")
bottom_frame.pack(side="bottom", fill="x", pady=10)

# Add a status bar at the bottom
status_var = tk.StringVar()
status_var.set(f"Selected color: Blue")
status_bar = tk.Label(root, textvariable=status_var, bd=1, relief="sunken", anchor="w", font=("Segoe UI", 10), bg="#f5f5f5")
status_bar.pack(side="bottom", fill="x")

def set_color(idx):
    global colorIndex
    colorIndex = idx
    color_names = ["Blue", "Green", "Red", "Yellow"]
    status_var.set(f"Selected color: {color_names[colorIndex]}")
    

# Use ttk for modern buttons
style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=("Segoe UI", 12, "bold"), padding=6)
style.map("TButton",
          relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

color_names = ["Blue", "Green", "Red", "Yellow"]
color_values = ["#0000FF", "#00FF00", "#FF0000", "#FFFF00"]
for i, (name, color) in enumerate(zip(color_names, color_values)):
    style.configure(f"{name}.TButton", background=color)
    btn = ttk.Button(
        bottom_frame,
        text=name,
        style=f"{name}.TButton",
        command=lambda i=i: set_color(i)
    )
    btn.pack(side="left", padx=8, pady=5)

def clear_canvas():
    global bpoints, gpoints, rpoints, ypoints, blue_index, green_index, red_index, yellow_index, paintWindow
    bpoints = [deque(maxlen=1024)]
    gpoints = [deque(maxlen=1024)]
    rpoints = [deque(maxlen=1024)]
    ypoints = [deque(maxlen=1024)]
    blue_index = green_index = red_index = yellow_index = 0
    paintWindow[67:, :, :] = 255  # Reset to white background
    status_var.set("Canvas cleared!")

clear_btn = ttk.Button(
    bottom_frame,
    text="Clear Canvas",
    style="TButton",
    command=clear_canvas
)
clear_btn.pack(side="left", padx=15, pady=5)

root.bind("<Escape>", lambda e: root.destroy())

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, PANEL_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, PANEL_HEIGHT)

def update():
    global bpoints, gpoints, rpoints, ypoints
    global blue_index, green_index, red_index, yellow_index, colorIndex
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (PANEL_WIDTH, PANEL_HEIGHT))
        h, w, c = frame.shape

        # Draw color buttons on frame
        cv2.rectangle(frame, (40, 1), (140, 60), (128, 128, 128), 2)
        cv2.rectangle(frame, (160, 1), (255, 60), (255, 0, 0), 2)
        cv2.rectangle(frame, (275, 1), (370, 60), (0, 255, 0), 2)
        cv2.rectangle(frame, (390, 1), (485, 60), (0, 0, 255), 2)
        cv2.rectangle(frame, (505, 1), (600, 60), (0, 255, 255), 2)
        cv2.rectangle(frame, (160, 1), (255, 60), (255, 0, 0), -1)
        cv2.rectangle(frame, (275, 1), (370, 60), (0, 255, 0), -1)
        cv2.rectangle(frame, (390, 1), (485, 60), (0, 0, 255), -1)
        cv2.rectangle(frame, (505, 1), (600, 60), (0, 255, 255), -1)
        cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)

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
                            paintWindow[67:, :, :] = 255  # Reset to white background
                            status_var.set("Canvas cleared!")
                        elif 160 <= center[0] <= 255:
                            colorIndex = 0  # Blue
                            status_var.set(f"Selected color: Blue")
                        elif 275 <= center[0] <= 370:
                            colorIndex = 1  # Green
                            status_var.set(f"Selected color: Green")
                        elif 390 <= center[0] <= 485:
                            colorIndex = 2  # Red
                            status_var.set(f"Selected color: Red")
                        elif 505 <= center[0] <= 600:
                            colorIndex = 3  # Yellow
                            status_var.set(f"Selected color: Yellow")
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
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)
        video_panel.imgtk = imgtk
        video_panel.configure(image=imgtk)

        # Show persistent canvas
        canvas_img = Image.fromarray(cv2.cvtColor(paintWindow, cv2.COLOR_BGR2RGB))
        canvas_imgtk = ImageTk.PhotoImage(image=canvas_img)
        canvas_panel.imgtk = canvas_imgtk
        canvas_panel.configure(image=canvas_imgtk)

    root.after(1, update)

update()
root.mainloop()
cap.release()
cv2.destroyAllWindows()



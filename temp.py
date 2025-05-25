import site
print(site.getsitepackages())


# # C:\\Users\\shrey\\AppData\\Roaming\\Python\\Python310\\site-packages\\mediapipe
# # C:\\Users\\shrey\\AppData\\Roaming\\Python\\Python310\\site-packages\\cv2


# python -m PyInstaller --onefile --windowed ^
#     --hidden-import=PIL 
#     --hidden-import=PIL._tkinter_finder 
#     --hidden-import=cv2 
#     --hidden-import=mediapipe 
#     --hidden-import=numpy 
#     --add-data "C:\\Users\\shrey\\AppData\\Roaming\\Python\\Python310\\site-packages\\mediapipe;mediapipe" 
#     --add-data "C:\\Users\\shrey\\AppData\\Roaming\\Python\\Python310\\site-packages\\cv2;cv2" air_canvas_tkinter_app.py


# python -m PyInstaller --onefile --windowed --hidden-import=PIL --hidden-import=PIL._tkinter_finder --hidden-import=cv2 --hidden-import=mediapipe --hidden-import=numpy --add-data "\\Users\\shrey\\AppData\\Roaming\\Python\\Python310\\site-packages\\mediapipe:mediapipe" --add-data "C:\\Users\\shrey\\AppData\\Roaming\\Python\\Python310\\site-packages\\cv2:cv2" air_canvas_tkinter_app.py


# python -m PyInstaller --onefile --windowed ^
# --hidden-import=PIL ^
# --hidden-import=PIL._tkinter_finder ^
# --hidden-import=cv2 ^
# --hidden-import=mediapipe ^
# --hidden-import=numpy ^
# --add-data="C:\\Users\\shrey\\AppData\\Roaming\\Python\\Python310\\site-packages\\mediapipe":mediapipe ^
# --add-data="C:\\Users\\shrey\\AppData\\Roaming\\Python\\Python310\\site-packages\\cv2":cv2^
# air_canvas_tkinter_app.py


# ['C:\\Program Files\\Python310', 'C:\\Program Files\\Python310\\lib\\site-packages']
#  'C:\\Program Files\\Python310\\lib\\site-packages'

# python -m PyInstaller --onefile --windowed --hidden-import=PIL --hidden-import=PIL._tkinter_finder --hidden-import=cv2 --hidden-import=mediapipe --hidden-import=numpy --add-data="C:\\Program Files\\Python310\\lib\\site-packages\\mediapipe":mediapipe --add-data="C:\\Program Files\\Python310\\lib\\site-packages\\cv2":cv2 air_canvas_tkinter_app.py

# pyinstaller --onefile --windowed --hidden-import=PIL --hidden-import=PIL._tkinter_finder --hidden-import=cv2 --hidden-import=mediapipe --hidden-import=numpy --add-data="C:\\Program Files\\Python310\\lib\\site-packages\mediapipe:mediapipe" --add-data="C:\\Program Files\\Python310\\lib\\site-packages\cv2:cv2" air_canvas_tkinter_app.py

12
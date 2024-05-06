import cv2
import os
import mediapipe as mp
import numpy as np
from utils.draw_styled_landmarks import draw_styled_landmarks as dslandmarks
from utils.mediapipe_detection import mediapipe_detection as mpdetection
from utils.extract_keypoints import extract_keypoints
from settings.create_model import DATA_PATH, existing_label_map, new_actions_with_labels, no_sequences, sequence_length

mp_holistic = mp.solutions.holistic 
mp_drawing = mp.solutions.drawing_utils 
#########################################################
label_map_path = os.path.join(DATA_PATH, "label_map.txt")
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)
    with open(label_map_path, "w") as f:
        for action, label in new_actions_with_labels.items():
            f.write(f"{action}:{label}\n")
    print("Etiket Haritası Oluşturuldu:")
    print(new_actions_with_labels)
existing_label_map = {}
if os.path.exists(label_map_path):
    with open(label_map_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            action, label = line.strip().split(":")
            existing_label_map[action] = int(label)
for action, label in new_actions_with_labels.items():
    if action not in existing_label_map:
        existing_label_map[action] = label
with open(label_map_path, "w") as f:
    for action, label in existing_label_map.items():
        f.write(f"{action}:{label}\n")
print("Güncellenmiş Etiket Haritası:")
print(existing_label_map)
actions = np.array(list(existing_label_map.keys()))
#########################################################

cap = cv2.VideoCapture(0)

with mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    for action, label in new_actions_with_labels.items():
        for sequence in range(no_sequences):
            for frame_num in range(sequence_length):
                ret, frame = cap.read()
                image, results = mpdetection(frame, holistic)
                dslandmarks(image, results, mp_holistic, mp_drawing)
                if frame_num == 0: 
                    cv2.putText(image, 'STARTING COLLECTION', (120,200), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 4, cv2.LINE_AA)
                    cv2.putText(image, 'Collecting frames for {} Video Number {}'.format(action, sequence), (15,12), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.imshow('OpenCV Feed', image)
                    cv2.waitKey(2000)
                else: 
                    cv2.putText(image, 'Collecting frames for {} Video Number {}'.format(action, sequence), (15,12), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.imshow('OpenCV Feed', image)
                
                folder_path = os.path.join(DATA_PATH, action, str(sequence))
                os.makedirs(folder_path, exist_ok=True)
                
                keypoints = extract_keypoints(results)
                npy_path = os.path.join(folder_path, str(frame_num) + '.npy')
                np.save(npy_path, keypoints)
                
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
cap.release()
cv2.destroyAllWindows()
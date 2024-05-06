from fastapi import FastAPI, Form
app = FastAPI()
import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model # type: ignore
from utils.mediapipe_detection import mediapipe_detection as mpdetection
from utils.extract_keypoints import extract_keypoints
from utils.draw_styled_landmarks import draw_styled_landmarks as dslandmarks
from utils.base64_to_image import base64_to_image
from utils.prob_viz import prob_viz, colors
from settings.create_model import actions, keras_model_name

model = load_model(keras_model_name)

#image_url = "https://www.shutterstock.com/image-photo/old-man-making-out-hands-260nw-551186926.jpg"
#image = url_to_image(image_url)

def predictWithBase64(img: str, openWindow: bool = False):
    image = base64_to_image(img)

    mp_holistic = mp.solutions.holistic 
    mp_drawing = mp.solutions.drawing_utils 

    sequence = []
    sentence = []
    predictions = []
    threshold = 0.5

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        image, results = mpdetection(image, holistic)
            
        dslandmarks(image, results, mp_holistic, mp_drawing)
            
        keypoints = extract_keypoints(results)
        sequence = [keypoints] * 30 
            
        res = model.predict(np.expand_dims(sequence, axis=0))[0]

        if openWindow:
            predictions.append(np.argmax(res))
                
            if np.unique(predictions[-10:])[0]==np.argmax(res): 
                if res[np.argmax(res)] > threshold: 
                    if len(sentence) > 0: 
                        if actions[np.argmax(res)] != sentence[-1]:
                            sentence.append(actions[np.argmax(res)])
                    else:
                        sentence.append(actions[np.argmax(res)])

            if len(sentence) > 5: 
                sentence = sentence[-5:]

            image = prob_viz(res, actions, image, colors)
                
            cv2.rectangle(image, (0,0), (640, 40), (245, 117, 16), -1)
            cv2.putText(image, ' '.join(sentence), (3,30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                
            cv2.imshow('OpenCV Feed', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return actions[np.argmax(res)]
    

@app.post("/")
def predict(base64_code: str = Form()):
    prediction = predictWithBase64(base64_code)
    return {"prediction": prediction}



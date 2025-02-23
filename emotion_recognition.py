import cv2
import numpy as np
from scipy.ndimage import zoom
from scipy.spatial import distance
import mediapipe as mp
from keras.models import load_model
from moviepy.editor import VideoFileClip
from fer.utils import draw_annotations
from fer import FER
import statistics
from imutils import face_utils

global shape_x
global shape_y
global input_shape
global nClasses
# we need this to initialise the points for the face
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


def detect_facial_landmarks(frame): 
      rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      results = face_mesh.process(rgb_frame)
      landmarks_points = []
      if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:# this is in case there are multiple faces
            for lm in face_landmarks.landmark:
                #converting the normalized coordinates to pixel coordinates
                x = int(lm.x * frame.shape[1])
                y = int(lm.y * frame.shape[0])
                landmarks_points.append((x, y))
      return gray, landmarks_points
          
def stabilize_face(frame, landmarks):
    if not landmarks:
        return frame
    #how we find the bounding box
    xs = [pt[0] for pt in landmarks]
    ys = [pt[1] for pt in landmarks]
    x_min = max(min(xs) - 10, 0)
    y_min = max(min(ys) - 10, 0)
    x_max = min(max(xs) + 10, frame.shape[1])
    y_max = min(max(ys) + 10, frame.shape[0])
    face_roi = frame[y_min:y_max, x_min:x_max]
    gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    
    #apply CLAHE for brightness normalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized_face = clahe.apply(gray_face)
    
    #fancy gaussin blurrr
    smoothed_face = cv2.GaussianBlur(equalized_face, (3, 3), 0)
    
    #concert back tobgr 
    stabilized_face = cv2.cvtColor(smoothed_face, cv2.COLOR_GRAY2BGR)
    frame[y_min:y_max, x_min:x_max] = stabilized_face
    
    return frame

def show_webcam():
  detector = FER()
  video_capture = cv2.VideoCapture(0)
  if not video_capture.isOpened():
        print("Error: Could not open webcam.")
        return
  pred_buffer = []
  buffer_size = 10 
  emotion_list = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
  counter= 0
  while True:
    #frame by frame
    ret, frame = video_capture.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    _, landmarks = detect_facial_landmarks(frame)
    for (x, y) in landmarks:
        cv2.circle(frame, (x, y), 1, (220, 255, 200), -1)
    stabilized_frame = stabilize_face(frame, landmarks)
    emotions = detector.detect_emotions(stabilized_frame)
    if(emotions):
        emotion_values = list(emotions[0]['emotions'].values())
        emotions_arr = np.array([value for value in emotion_values])
        prediction_result = np.argmax(emotions_arr)
        pred_buffer.append(prediction_result)
        if len(pred_buffer) > buffer_size:
            pred_buffer.pop(0)
        try:
            stable_emotion = statistics.mode(pred_buffer)
        except statistics.StatisticsError:
            stable_emotion = prediction_result
        cv2.putText(frame, f"Emotion: {emotion_list[stable_emotion]}", (30, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # frame = draw_annotations(frame, emotions)
    cv2.imshow("Webcam - MediaPipe Face Mesh", frame)
    
    #exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    counter +=1

  video_capture.release()
  cv2.destroyAllWindows()
  return emotion_list[stable_emotion]

  
# def main():
#     show_webcam()

# if __name__ == "__main__":
#     main()

      
  
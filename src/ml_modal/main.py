import cv2
import numpy as np
from keras.models import load_model

# Load the pre-trained emotion detection model
emotion_model = load_model('src\ml_modal\model.h5')

# Load the Haar Cascades classifier for face detection
face_cascade = cv2.CascadeClassifier('src\ml_modal\haarcascade_frontalface_default.xml')

# Define a function to detect and classify emotions in a face
def detect_emotion(img):
    if img is None or img.size == 0:
        return img
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    
    # For each detected face, classify the emotion using the pre-trained model
    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (48, 48))
        face_img = np.reshape(face_img, (1, 48, 48, 1))
        face_img = face_img / 255.0
        
        prediction = emotion_model.predict(face_img)
        max_index = np.argmax(prediction[0])
        emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        emotion = emotions[max_index]
        
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(img, emotion, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    return img

# Create a video capture object
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the video stream
    ret, frame = cap.read()
    
    # Detect and classify emotions in the frame
    frame = detect_emotion(frame)
    
    # Display the resulting frame
    cv2.imshow('Emotion Detection', frame)
    
    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the windows
cap.release()
cv2.destroyAllWindows()

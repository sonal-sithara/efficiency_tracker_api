from flask import Blueprint, jsonify, request
import cv2
from tensorflow import keras
import numpy as np
import base64

# Load pre-trained model
model = keras.models.load_model('src\ml_modal\model.h5')

# Load Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier('src\ml_modal\haarcascade_frontalface_default.xml')

mlCtrl = Blueprint('ml', __name__)

@mlCtrl.route('/emotion-recognition', methods=['POST'])

def recognize_emotion():
    # Read base64-encoded image from client
    image_b64 = request.json.get('image')
    img_bytes = base64.b64decode(image_b64)
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Initialize list to store results
    results = []

    # Iterate through each face and predict emotion
    for (x, y, w, h) in faces:
        # Crop face region
        face = gray[y:y+h, x:x+w]

        # Resize face to match input size of model
        face = cv2.resize(face, (48, 48))

        # Normalize pixel values
        face = face / 255.0

        # Reshape to match input shape of model
        face = face.reshape(1, 48, 48, 1)

        # Predict emotion using model
        emotion = model.predict(face)[0]

        # Map predicted probabilities to emotion labels
        emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        emotion_label = emotions[np.argmax(emotion)]

        # Add emotion result to results list
        results.append({'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h), 'emotion': emotion_label})

    # Return results as JSON
    return jsonify(results)
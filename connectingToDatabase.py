# -*- coding: utf-8 -*-
"""
Created on Sat Sep 2 05:03:03 2023

@author: Syed Mahir Faisal and Mahbubur Rahman Rafi
"""
import cv2

import statistics
import mysql.connector
import webbrowser
from deepface import DeepFace


emotion_predictions = []
prediction_count = 0
# Connect to MySQL
connection = mysql.connector.connect(
      host="localhost",
      user="root",  # username
      password="admin",  # password
      database="pyconn"
  )


face_cascade = cv2.CascadeClassifier(
    'D:\Project\haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    result = DeepFace.analyze(img_path=frame, actions=[
                              'emotion'], enforce_detection=False)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)

    emotion = result[0]['dominant_emotion']

    txt = str(emotion)

    cv2.putText(frame, txt, (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    cv2.imshow('Emotion Detection', frame)
    emotion_predictions.append(emotion)
    prediction_count += 1
    max_predictions = 100
    if prediction_count >= max_predictions:
        break
    if cv2.waitKey(1) & 0xff == ord('r'):
        break
cap.release()
cv2.destroyAllWindows()


if emotion_predictions:
    average_emotion = statistics.mode(emotion_predictions)
else:
    average_emotion = "No emotions detected"

    
# Create a cursor
cursor = connection.cursor()

# Fetch the results
select_query = "SELECT Url FROM table1 WHERE Emotion = %s"
mood = average_emotion

cursor.execute(select_query, (mood,))

result = cursor.fetchone()
if result:
    Link = result[0]

else:
    print("No matching record found.")

# Define the URL you want to open

# Add a URL of JavaTpoint to open it in a browser
url = Link
# Open the URL using open() function of module
webbrowser.open_new_tab(url)

cursor.close()
connection.close()
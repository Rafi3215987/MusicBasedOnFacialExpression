import cv2
import statistics
from deepface import DeepFace
import webbrowser
import mysql.connector

class EmotionDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.emotion_predictions = []
        self.prediction_count = 0
        self.max_predictions = 100

    def detect_emotion(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            result = DeepFace.analyze(img_path=frame, actions=['emotion'], enforce_detection=False)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)

            emotion = result[0]['dominant_emotion']

            txt = str(emotion)

            cv2.putText(frame, txt, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            cv2.imshow('Emotion Detection', frame)
            self.emotion_predictions.append(emotion)
            self.prediction_count += 1

            if self.prediction_count >= self.max_predictions:
                break

            if cv2.waitKey(1) & 0xff == ord('r'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def get_emotion_predictions(self):
        return self.emotion_predictions

class EmotionAverageCalculator:
    def calculate_average_emotion(self, emotion_predictions):
        if emotion_predictions:
            return statistics.mode(emotion_predictions)
        else:
            return "No emotions detected"

class DatabaseConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, params)
                return cursor
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return None

class URLRetriever:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def retrieve_url(self, emotion):
        select_query = "SELECT playlist FROM playlist WHERE Emotion = %s"
        cursor = self.db_connector.execute_query(select_query, (emotion,))
        
        if cursor:
            result = cursor.fetchone()
            if result:
                return result[0]
        
        return "No matching record found."

class EmotionAnalysisApp:
    def __init__(self):
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = "galidimuna"
        self.db_name = "pyconn"

    def run(self):
        detector = EmotionDetector()
        detector.detect_emotion()
        emotion_predictions = detector.get_emotion_predictions()

        average_calculator = EmotionAverageCalculator()
        average_emotion = average_calculator.calculate_average_emotion(emotion_predictions)

        db_connector = DatabaseConnector(self.db_host, self.db_user, self.db_password, self.db_name)
        if db_connector.connect():
            url_retriever = URLRetriever(db_connector)
            url = url_retriever.retrieve_url(average_emotion)
            
            if url != "No matching record found.":
                webbrowser.open_new_tab(url)
            
            db_connector.disconnect()
        else:
            print("Failed to connect to the database.")

if __name__ == "__main__":
    app = EmotionAnalysisApp()
    app.run()

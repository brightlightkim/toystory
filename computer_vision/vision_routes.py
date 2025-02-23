# from flask import Flask, Response, jsonify
# import cv2
# from vision_controller import MoodAnalyzer
# By Ujjwal Gupta
# app = Flask(__name__)
# mood_analyzer = MoodAnalyzer()

# def generate_frames():
#     cap = cv2.VideoCapture(0)

#     while cap.isOpened():
#         success, frame = cap.read()
#         if not success:
#             break

#         processed_frame, emotion = mood_analyzer.process_frame(frame)

#         # Encode frame for web streaming
#         _, buffer = cv2.imencode('.jpg', processed_frame)
#         frame_bytes = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     cap.release()

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/emotion')
# def get_emotion():
#     return jsonify({"emotion": mood_analyzer.analyze_emotions()})

# if __name__ == "__main__":
#     app.run(debug=True)

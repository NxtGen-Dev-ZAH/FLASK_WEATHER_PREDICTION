from flask import Flask, make_response, request, jsonify, render_template
import os
import requests

FLASK_ENV = os.getenv("FLASK_ENV")
FLASK_DEBUG = os.getenv("FLASK_DEBUG")

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    # return {"message": "Welcome Zaheer Ahmed Abbasi"}, 200
    return render_template("index.html")


@app.route("/json", methods=["POST"])
def json_example():
    data = request.get_json()
    return jsonify({"received_data": data})


@app.route("/user/<username>")
def user_profile(username):
    return render_template("profile.html", userna56=username)


# direct name likha jai ga browser url me.


@app.route("/search")
def search():
    query = request.args.get("q", "")
    return f"Searching for: {query}"


# /search?q=zaheer


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Check if the POST request has a file part
        if "file" not in request.files:
            return render_template("uploads.html", error="No file part")

        file = request.files["file"]

        # If the user does not select a file, browser also submits an empty part
        if file.filename == "":
            return render_template("uploads.html", error="No selected file")

        # Save the uploaded file
        file.save(f"uploads/{file.filename}")
        return "File uploaded successfully!"

    return render_template("uploads.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


# {
#     "emotionPredictions": [
#         {
#             "emotion": {
#                 "anger": 0.0043079085,
#                 "disgust": 0.00041127237,
#                 "fear": 0.0037504788,
#                 "joy": 0.9918804,
#                 "sadness": 0.014091322,
#             },
#             "target": "",
#             "emotionMentions": [
#                 {
#                     "span": {
#                         "begin": 0,
#                         "end": 30,
#                         "text": "i am so happy i am doing this ",
#                     },
#                     "emotion": {
#                         "anger": 0.0043079085,
#                         "disgust": 0.00041127237,
#                         "fear": 0.0037504788,
#                         "joy": 0.9918804,
#                         "sadness": 0.014091322,
#                     },
#                 }
#             ],
#         }
#     ],
#     "producerId": {"name": "Ensemble Aggregated Emotion Workflow", "version": "0.0.1"},
# }


# @app.route("/emotionDetector", methods=["POST"])
# def evaluate_emotion():
#     if request.method == "POST":
#         text_to_analyze = request.form["text"]
#         result = emotion_detector(text_to_analyze)
#         return jsonify(
#             {
#                 "response": f"For the given statement, the system response is {result['emotion_scores']}. The dominant emotion is {result['dominant_emotion']}."
#             }
#         )
#     return make_response("functION is not working")


from flask import Flask, request, jsonify
from flask_cors import CORS
from main import predictMessage, explainMessage, getSuspiciousWords

app = Flask(__name__)
CORS(app)

@app.route("/detect", methods=["POST"])
def scan():
    message = request.json["message"]

    prediction = predictMessage(message)
    explanation = explainMessage(message, prediction)

    return jsonify({
        "prediction": prediction,
        "explanation": explanation
    })

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from main import predictMessage, explainMessage, getSuspiciousWords

app = Flask(__name__)
CORS(app)

#post request gathering responses to entered message
@app.route("/detect", methods=["POST"])
def scan():
    message = request.json["message"]

    suspicious = getSuspiciousWords(message)
    words = [word for word, weight in suspicious]
    
    prediction = predictMessage(message)
    explanation = explainMessage(message, prediction)

    return jsonify({
        "prediction": prediction,
        "explanation": explanation,
        "suspiciousWords": words
    })

if __name__ == "__main__":
    app.run(debug=True)
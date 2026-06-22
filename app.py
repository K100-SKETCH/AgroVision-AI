from flask import Flask, render_template, request
import os
from datetime import datetime

from predict import predict_disease
from disease_info import DISEASE_INFO

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    image = request.files["leaf_image"]

    if image:

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            image.filename
        )

        image.save(filepath)

        disease, confidence = predict_disease(
            filepath
        )

        print("Predicted Disease:", disease)

        info = DISEASE_INFO.get(
            disease,
            {
                "symptoms": "Information not available",
                "treatment": "Information not available",
                "prevention": "Information not available"
            }
        )

        confidence = round(confidence, 2)

        if confidence >= 90:
            reliability = "High Confidence"

        elif confidence >= 70:
            reliability = "Medium Confidence"

        else:
            reliability = "Low Confidence"

        analysis_time = datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )

        return render_template(
            "result.html",
            disease=disease,
            confidence=confidence,
            reliability=reliability,
            analysis_time=analysis_time,
            image_path=filepath,
            symptoms=info["symptoms"],
            treatment=info["treatment"],
            prevention=info["prevention"]
        )

    return "Upload Failed"


if __name__ == "__main__":
    app.run(debug=True)
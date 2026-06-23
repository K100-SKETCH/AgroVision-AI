from flask import Flask, render_template, request
import os
import time
from datetime import datetime

from predict import predict_disease
from disease_info import DISEASE_INFO

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    print("HOME PAGE OPENED", flush=True)
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    print("=" * 60, flush=True)
    print("UPLOAD REQUEST RECEIVED", flush=True)

    try:

        image = request.files.get("leaf_image")

        if image is None:
            return "No image uploaded"

        filename = image.filename

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        image.save(filepath)

        print("IMAGE SAVED", flush=True)

        disease, confidence = predict_disease(filepath)

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

    except Exception as e:

        print("ERROR:", str(e), flush=True)

        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )

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
    print("HOME PAGE OPENED")
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    print("=" * 60)
    print("UPLOAD REQUEST RECEIVED")

    start_time = time.time()

    try:

        image = request.files.get("leaf_image")

        if not image:
            print("NO IMAGE RECEIVED")
            return "No image uploaded"

        print("Image Name:", image.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            image.filename
        )

        print("Saving image...")

        image.save(filepath)

        print("Image saved at:", filepath)

        prediction_start = time.time()

        print("STARTING PREDICTION...")

        disease, confidence = predict_disease(filepath)

        prediction_end = time.time()

        print("PREDICTION COMPLETE")
        print(
            f"Prediction Time: {round(prediction_end - prediction_start, 2)} seconds"
        )

        print("Disease:", disease)
        print("Confidence:", confidence)

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

        total_time = round(time.time() - start_time, 2)

        print(f"TOTAL REQUEST TIME: {total_time} seconds")
        print("=" * 60)

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

        print("ERROR OCCURRED")
        print(str(e))

        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000,
        debug=True
    )

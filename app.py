from flask import Flask, render_template, request
import os
import time
from datetime import datetime
import psutil

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


@app.route("/memory")
def memory():

    process = psutil.Process()

    return {
        "memory_mb":
        round(
            process.memory_info().rss / 1024 / 1024,
            2
        )
    }


@app.route("/upload", methods=["POST"])
def upload():

    print("=" * 60, flush=True)
    print("UPLOAD REQUEST RECEIVED", flush=True)

    start_time = time.time()

    try:

        image = request.files.get("leaf_image")

        if not image:
            return "No image uploaded"

        print(f"IMAGE RECEIVED: {image.filename}", flush=True)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            image.filename
        )

        image.save(filepath)

        print(f"IMAGE SAVED: {filepath}", flush=True)

        print("CALLING PREDICT_DISEASE()", flush=True)

        disease, confidence = predict_disease(filepath)

        print("PREDICTION RETURNED", flush=True)

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

        print(
            f"TOTAL REQUEST TIME: {round(time.time()-start_time,2)} sec",
            flush=True
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

        print("ERROR IN APP.PY", flush=True)
        print(str(e), flush=True)

        return f"ERROR: {str(e)}"


@app.route("/test")
def test():
    return "Flask is working"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )

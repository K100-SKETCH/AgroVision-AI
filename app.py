from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    print("HOME PAGE OPENED", flush=True)
    return render_template("index.html")


@app.route("/test")
def test():
    print("TEST ROUTE HIT", flush=True)
    return "Flask is working"


@app.route("/upload", methods=["POST"])
def upload():

    print("=" * 60, flush=True)
    print("UPLOAD REQUEST RECEIVED", flush=True)

    try:

        image = request.files.get("leaf_image")

        if image is None:
            print("NO IMAGE RECEIVED", flush=True)
            return "No image uploaded"

        print("IMAGE RECEIVED:", image.filename, flush=True)

        filename = image.filename

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        print("SAVING IMAGE...", flush=True)

        image.save(filepath)

        print("IMAGE SAVED:", filepath, flush=True)

        print("UPLOAD TEST SUCCESS", flush=True)

        return f"""
        <h1>Upload Successful ✅</h1>
        <p>File: {filename}</p>
        <p>Saved at: {filepath}</p>
        """

    except Exception as e:

        print("ERROR:", str(e), flush=True)

        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )

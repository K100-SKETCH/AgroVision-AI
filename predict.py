import time
import numpy as np
from PIL import Image

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input


MODEL_PATH = "model/agrovision_best_model.h5"

print("Loading model...")
model = load_model(MODEL_PATH)
print("Model loaded successfully!")


CLASS_NAMES = [
    "Pepper Bell Bacterial Spot",
    "Pepper Bell Healthy",
    "Potato Early Blight",
    "Potato Late Blight",
    "Potato Healthy",
    "Tomato Bacterial Spot",
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Tomato Leaf Mold",
    "Tomato Septoria Leaf Spot",
    "Tomato Spider Mites",
    "Tomato Target Spot",
    "Tomato Yellow Leaf Curl Virus",
    "Tomato Mosaic Virus",
    "Tomato Healthy"
]


def predict_disease(image_path):

    print("=" * 50)
    print("PREDICTION FUNCTION STARTED")

    start_time = time.time()

    print("Opening image...")
    img = Image.open(image_path).convert("RGB")

    print("Resizing image...")
    img = img.resize((224, 224))

    print("Converting image to numpy array...")
    img_array = np.array(img)

    print("Adding batch dimension...")
    img_array = np.expand_dims(img_array, axis=0)

    print("Preprocessing image...")
    img_array = preprocess_input(img_array)

    print("Running model.predict()...")
    predict_start = time.time()

    prediction = model.predict(
        img_array,
        verbose=0
    )

    predict_end = time.time()

    print(
        f"model.predict() completed in {round(predict_end - predict_start, 2)} seconds"
    )

    print("\nRaw Prediction:")
    for i, score in enumerate(prediction[0]):
        print(
            CLASS_NAMES[i],
            ":",
            round(float(score) * 100, 2),
            "%"
        )

    predicted_index = np.argmax(prediction)

    disease = CLASS_NAMES[predicted_index]

    confidence = float(
        np.max(prediction) * 100
    )

    total_time = round(
        time.time() - start_time,
        2
    )

    print("Predicted Disease:", disease)
    print("Confidence:", confidence)
    print(f"Total Prediction Time: {total_time} seconds")
    print("=" * 50)

    return disease, confidence

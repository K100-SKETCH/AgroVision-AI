import numpy as np
from PIL import Image

from tensorflow.keras.models import load_model

print("Loading model...", flush=True)

model = load_model(
    "model/agrovision_best_model.h5",
    compile=False
)

print("Model loaded successfully", flush=True)

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

    print("=" * 60, flush=True)
    print("FUNCTION ENTERED", flush=True)

    img = Image.open(image_path).convert("RGB")

    img = img.resize((224, 224))

    x = np.array(img).astype("float32")

    x = np.expand_dims(x, axis=0)

    print("BEFORE MODEL.PREDICT", flush=True)

    pred = model.predict(x, verbose=0)

    print("AFTER MODEL.PREDICT", flush=True)

    predicted_index = int(np.argmax(pred[0]))

    confidence = float(np.max(pred[0]) * 100)

    disease = CLASS_NAMES[predicted_index]

    print("PREDICTION COMPLETE", flush=True)

    return disease, confidence

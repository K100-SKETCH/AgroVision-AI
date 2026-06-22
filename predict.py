import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input

MODEL_PATH = "model/agrovision_best_model.h5"

model = load_model(MODEL_PATH)

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

    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)

    img_array = preprocess_input(img_array)

    prediction = model.predict(img_array)

    print("\nRaw Prediction:")
    for i, score in enumerate(prediction[0]):
        print(CLASS_NAMES[i], ":", round(float(score) * 100, 2), "%")

    predicted_index = np.argmax(prediction)

    disease = CLASS_NAMES[predicted_index]

    confidence = float(np.max(prediction) * 100)

    return disease, confidence
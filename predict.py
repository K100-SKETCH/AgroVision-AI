import time
import numpy as np
from PIL import Image

from tensorflow.keras.models import load_model

print("Loading model...")

model = load_model(
    "model/agrovision_best_model.h5",
    compile=False
)

print("Model loaded successfully")


def predict_disease(image_path):

    print("Testing TensorFlow only")

    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))

    x = np.array(img).astype("float32")
    x = np.expand_dims(x, axis=0)

    print("Before inference")

    output = model(x, training=False)

    print("After inference")

    return "Test", 99.0

import time
import numpy as np
from PIL import Image

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input

MODEL_PATH = "model/agrovision_best_model.h5"

print("Loading model...", flush=True)

load_start = time.time()

model = load_model(
    MODEL_PATH,
    compile=False
)

print(
    f"Model loaded successfully in {round(time.time()-load_start,2)} sec",
    flush=True
)

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

    print("\n" + "=" * 60, flush=True)
    print("PREDICTION FUNCTION STARTED", flush=True)

    try:

        print("STEP 1: Opening image", flush=True)

        img = Image.open(image_path).convert("RGB")

        print("STEP 2: Resizing image", flush=True)

        img = img.resize((224, 224))

        print("STEP 3: Converting image to numpy", flush=True)

        img_array = np.array(img)

        print("STEP 4: Expanding dimensions", flush=True)

        img_array = np.expand_dims(
            img_array,
            axis=0
        )

        print("STEP 5: Preprocessing image", flush=True)

        img_array = preprocess_input(
            img_array.astype(np.float32)
        )

        print(
            "Input Shape:",
            img_array.shape,
            flush=True
        )

        print(
            "Input Dtype:",
            img_array.dtype,
            flush=True
        )

        print("STEP 6: SKIPPING MODEL PREDICTION", flush=True)

        prediction = np.zeros((1, 15))

        prediction[0][6] = 0.95

        print("STEP 7: DUMMY PREDICTION CREATED", flush=True)

        predicted_index = int(
            np.argmax(prediction[0])
        )

        disease = CLASS_NAMES[predicted_index]

        confidence = float(
            np.max(prediction[0]) * 100
        )

        print(
            f"Predicted Disease: {disease}",
            flush=True
        )

        print(
            f"Confidence: {confidence}",
            flush=True
        )

        print("=" * 60, flush=True)

        return disease, confidence

    except Exception as e:

        print(
            f"ERROR INSIDE predict_disease(): {str(e)}",
            flush=True
        )

        raise e

import time
import numpy as np
from PIL import Image

from tensorflow.keras.models import load_model

print("Loading model...", flush=True)

model = load_model(
    "model/agrovision_best_model.h5",
    compile=False
)

print("Model loaded successfully", flush=True)


def predict_disease(image_path):

    print("=" * 60, flush=True)
    print("FUNCTION ENTERED", flush=True)

    try:

        print("TRY BLOCK STARTED", flush=True)

        print("IMAGE PATH:", image_path, flush=True)

        print("OPENING IMAGE...", flush=True)

        img = Image.open(image_path)

        print("IMAGE OPENED", flush=True)

        print("CONVERTING RGB...", flush=True)

        img = img.convert("RGB")

        print("RGB COMPLETE", flush=True)

        print("RESIZING...", flush=True)

        img = img.resize((224, 224))

        print("RESIZE COMPLETE", flush=True)

        x = np.array(img).astype("float32")

        print("NUMPY CONVERSION COMPLETE", flush=True)

        x = np.expand_dims(x, axis=0)

        print("EXPAND DIMS COMPLETE", flush=True)

        print("RETURNING TEST VALUE", flush=True)

        return "Tomato Healthy", 99.0

    except Exception as e:

        print(
            f"ERROR INSIDE predict.py: {str(e)}",
            flush=True
        )

        raise e

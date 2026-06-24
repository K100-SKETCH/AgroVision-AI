import tensorflow as tf

tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(1)

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

    x = np.array(img).astype(np.float32)

    x = np.expand_dims(
        x,
        axis=0
    )

    print("BEFORE MODEL CALL", flush=True)

    pred = model(
        x,
        training=False
    )

    print("MODEL CALL FINISHED", flush=True)

    pred = pred.numpy()

    print("NUMPY CONVERSION FINISHED", flush=True)

    predicted_index = int(
        np.argmax(pred[0])
    )

    confidence = float(
        np.max(pred[0]) * 100
    )

    disease = CLASS_NAMES[predicted_index]

    # TOP 3 PREDICTIONS

    top3_indices = pred[0].argsort()[-3:][::-1]

    top3_predictions = []

    for idx in top3_indices:

        top3_predictions.append(
            {
                "name": CLASS_NAMES[idx],
                "confidence": round(
                    float(pred[0][idx] * 100),
                    2
                )
            }
        )

    print(
        f"DISEASE = {disease}",
        flush=True
    )

    print(
        f"CONFIDENCE = {confidence}",
        flush=True
    )

    return disease, confidence, top3_predictions

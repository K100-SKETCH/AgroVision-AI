import tensorflow as tf

# Limit TensorFlow threads for deployment
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(1)

import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model


print("Loading AgroVision AI model...", flush=True)

model = load_model(
    "model/agrovision_best_model.h5",
    compile=False
)

print("Model loaded successfully", flush=True)


# ============================================================
# CLASS NAMES
# ============================================================

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


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_disease(image_path):

    print("=" * 60, flush=True)
    print("PREDICTION FUNCTION ENTERED", flush=True)

    try:

        # ----------------------------------------------------
        # OPEN IMAGE
        # ----------------------------------------------------

        img = Image.open(image_path).convert("RGB")

        print("IMAGE OPENED SUCCESSFULLY", flush=True)

        # ----------------------------------------------------
        # BASIC IMAGE VALIDATION
        # ----------------------------------------------------

        width, height = img.size

        print(
            f"IMAGE SIZE: {width} x {height}",
            flush=True
        )

        # Reject extremely small images
        if width < 100 or height < 100:

            validation_message = (
                "The uploaded image is too small. "
                "Please upload a clear image of a tomato, "
                "potato, or bell pepper leaf."
            )

            return None, 0, [], validation_message

        # ----------------------------------------------------
        # RESIZE IMAGE
        # ----------------------------------------------------

        img = img.resize((224, 224))

        x = np.array(img).astype(np.float32)

        x = np.expand_dims(
            x,
            axis=0
        )

        print("IMAGE PREPARED", flush=True)

        # ----------------------------------------------------
        # MODEL PREDICTION
        # ----------------------------------------------------

        print("CALLING MODEL...", flush=True)

        pred = model(
            x,
            training=False
        )

        print("MODEL CALL FINISHED", flush=True)

        pred = pred.numpy()

        print("NUMPY CONVERSION FINISHED", flush=True)

        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        predicted_index = int(
            np.argmax(pred[0])
        )

        confidence = float(
            np.max(pred[0]) * 100
        )

        disease = CLASS_NAMES[predicted_index]

        # ----------------------------------------------------
        # TOP 3 PREDICTIONS
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # LOGGING
        # ----------------------------------------------------

        print(
            f"DISEASE = {disease}",
            flush=True
        )

        print(
            f"CONFIDENCE = {confidence}",
            flush=True
        )

        print("=" * 60, flush=True)

        # ----------------------------------------------------
        # RETURN SUCCESS
        # ----------------------------------------------------

        return (
            disease,
            confidence,
            top3_predictions,
            None
        )

    except Exception as e:

        print(
            f"PREDICTION ERROR: {str(e)}",
            flush=True
        )

        validation_message = (
            "Unable to process this image. "
            "Please upload a clear image of a tomato, "
            "potato, or bell pepper leaf."
        )

        return (
            None,
            0,
            [],
            validation_message
        )

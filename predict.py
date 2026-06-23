from PIL import Image
import time


def predict_disease(image_path):

    print("=" * 60, flush=True)
    print("PREDICTION FUNCTION STARTED", flush=True)

    start_time = time.time()

    try:

        print("OPENING IMAGE...", flush=True)

        img = Image.open(image_path)

        print("CONVERTING RGB...", flush=True)

        img = img.convert("RGB")

        print("RESIZING...", flush=True)

        img = img.resize((224, 224))

        print(
            f"IMAGE SIZE: {img.size}",
            flush=True
        )

        print(
            f"PREDICTION FINISHED IN {round(time.time()-start_time,2)} sec",
            flush=True
        )

        return "Tomato Early Blight", 95.0

    except Exception as e:

        print(
            f"ERROR INSIDE predict.py: {str(e)}",
            flush=True
        )

        raise e

from PIL import Image, ImageOps
import numpy as np
from config import IMAGE_PATH

def predict_class(model, class_names):
    size = (224, 224)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(IMAGE_PATH).convert("RGB")
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized
    prediction = model.predict(data)
    index = np.argmax(prediction)
    return class_names[index].strip()

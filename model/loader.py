import tensorflow as tf
from config import MODEL_PATH, LABELS_PATH

def load_model_and_labels():
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    labels = open(LABELS_PATH, 'r').readlines()
    return model, labels

import time
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow_hub as hub
import numpy as np
import os
from flask_cors import CORS
from pymongo import MongoClient
import requests

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient('mongodb+srv://satya:12345@trashkun.dxsnir6.mongodb.net/?retryWrites=true&w=majority&appName=TrashKun')
db = client['TrashKun']
logs_collection = db['logs']

# Load the TensorFlow model
model = load_model("model.h5", custom_objects={'KerasLayer': hub.KerasLayer})
classes = os.listdir("/mnt/d/Academics/Projects/DL/TrashAI/dataset/")
n = len(classes)
label_ind = {i: classes[i] for i in range(n)}

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No images uploaded"})
    img_file = request.files["image"]
    img_path = "trash.jpeg"
    img_file.save(img_path)
    img_array = preprocess_image(img_path)
    try:
        predictions = model.predict(img_array)
        # os.remove(img_path)
        predList = predictions.tolist()
        l = [(predList[0][i], label_ind[i]) for i in range(n)]
        ans = max(l)
        print(ans)
        # Log prediction to MongoDB
        trash_can_id = request.form.get("trash_can_id")  
        log = {"trash_can_id": trash_can_id, "prediction": ans[1]}
        logs_collection.insert_one(log)
        if(ans[1] in ["biological","cardboard","clothes","paper"]):
            return "1"
        else:
            return "0"
            
    except Exception as e:
        # os.remove(img_path)
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0")

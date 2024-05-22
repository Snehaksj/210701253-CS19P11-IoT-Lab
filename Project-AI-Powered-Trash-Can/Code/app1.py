import time
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)
CORS(app)

# api="http://192.168.0.105:5000/" 
api= "http://192.168.182.184:5000/"

@app.route("/capture_and_predict", methods=["GET"])
def capture_and_predict():
    try:
        response=requests.post(api+"capture",data="capture")
        time.sleep(1)
        if(response.status_code==200):
            image_file = {'image': open('trash.jpeg', 'rb')}
            if image_file:
                response = requests.post("http://localhost:5000/predict", files=image_file, data={"trash_can_id": "12345612"})
                if response.status_code == 200:
                    print("Response: ",response.text)
                    return response.text
                else:
                    return "Error processing image"
            else:
                return "Failed to capture image"
        else:
            return "Post req to caputre Failed"
        
    except Exception as e:
        return "Error capturing image: " + str(e)

@app.route("/capture_image", methods=["POST"])
def capture_image():
    try:
        image_data = request.data.decode('utf-8').split(",")[1]  # Extract the base64 string from the data
        image_bytes = base64.b64decode(image_data)
        
        # Code to save the image to the file system
        with open("trash.jpeg", "wb") as f:
            f.write(image_bytes)
        
        return jsonify({"message": "Image captured and saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

data=None
@app.route("/capture",methods=["POST","GET"])
def capture():
    global data
    if(request.method=="POST"):
        try:
            data="1"
            print("Innn")
            return jsonify({"stat":"ok"}),200
        except Exception as e:
            return jsonify({"error":str(e)}),500
    elif(request.method=="GET"):
        try:
            print("In get")
            if(data!=None):
                temp=data
                data=None
                return "1",200               
            else:
                return jsonify({"res":"no data"}),200
        except Exception as e:
            return jsonify({"error":str(e)}),500

HTML_DIRECTORY = "./"


@app.route("/camera")
def camera():
    return send_from_directory(HTML_DIRECTORY, "index.html")

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")

from flask import Flask, render_template, request, jsonify
import base64
from io import BytesIO
from PIL import Image
#from paddleocr import PaddleOCR
from pymongo import MongoClient
from pymongo.server_api import ServerApi
paddle = PaddleOCR(lang="en", ocr_version="PP-OCRv4", show_log=False)

app = Flask(__name__)
uri = "mongo link here"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client["test"]
collection = db["customer"]
def scanner(image_path):
    result = paddle.ocr(image_path, cls=True)
    result = result[0]
    texts = [line[1][0] for line in result]
    text_joined = " ".join(texts)
    return text_joined

@app.route("/upload", methods=["GET"])
def home():
    return render_template('home.html')

@app.route("/upload", methods=["POST"])
def uploadUtility():
    if 'image' not in request.files:
        return jsonify({"error": "No image data"}), 400
    image_data = request.files.get('image')
    image = Image.open(image_data)
    vehicle_id = scanner(image)
    data = collection.find_one({"vehicleID" : vehicle_id});
    if data is not None:
        return {"success": True,data: "Valid Vehicle ID"};
    return {"success": False,data: "Invalid Vehicle ID"};

if __name__ == '__main__':
    app.run(debug=True)


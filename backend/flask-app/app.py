from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import sys

MODEL_DIR = '/home/vivaan/Desktop/projects/Machine+DeepLearning/video-game-classifier/Video-Game-Classifier/backend/machine-learning-utls/model'
STATIC_DIR = '/home/vivaan/Desktop/projects/Machine+DeepLearning/video-game-classifier/Video-Game-Classifier/backend/flask-app/templates/static'
sys.path.append(MODEL_DIR)

from predict import *

app = Flask(__name__, static_folder=STATIC_DIR)
cors=CORS(app)
app.config["CORS_HEADERS"] = 'Content-Type'

"""A POST request to get the predicted label of the game image inputted
Returns the name of the game as a string
Returns:
    _type_: str
"""
@app.route("/get_prediction", methods = ["POST"])
@cross_origin()
def handle_form():
    image = request.files['image']
    image.save(f'{STATIC_DIR}/image.jpeg')
    pred = predict()
    return pred

if __name__ == "__main__":
    app.run(port=8080)
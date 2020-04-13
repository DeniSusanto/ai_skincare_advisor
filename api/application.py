from flask import Flask, request
# from acne_detection import AcneDetector
from age_gender_estimation import AgeGenderEstimator
from dark_eye_detection import DarkEyeDetector
from facial_landmark import FacialLandmark
from wrinkles_detection import WrinklesDetector
from recommendation_system import ProductRecommendation
import cv2
import base64
import numpy as np
from PIL import Image
import io
import pandas as pd
import json

application = Flask(__name__)


def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))


def toRGB(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)


@application.route('/')
def index():
    return 'Server is running!'


@application.route('/score', methods=['POST'])
def score_image():
    img_string = request.values['image']
    ori_img = toRGB(stringToImage(img_string))
    fl = FacialLandmark(ori_img)

    ag = AgeGenderEstimator(fl)
    age_gender = ag.predict_age_gender()

    de = DarkEyeDetector(fl)
    r, l = de.get_dark_eyes()
    dark_eye_score = de.get_score()

    # ad = AcneDetector(fl)
    # acne_score = ad.get_overall_score()

    wd = WrinklesDetector(fl)
    wrinkle_score = wd.get_overall_score()

    return {
        'statusCode': 200,
        'body': {
            'age-gender': age_gender,
            'dark-eye': dark_eye_score,
            # 'acne': acne_score,
            'wrinkle': wrinkle_score
        }
    }


@application.route('/recommendation', methods=['POST'])
def get_recommendation():
    catalogue = pd.read_csv('product_catalogue.csv')
    json_input = request.get_json()
    rec = ProductRecommendation(catalogue, json_input)
    results = rec.get_default_recommendation()

    return {
        'statusCode': 200,
        'body': results
    }


if __name__ == '__main__':
    application.run(debug=False)

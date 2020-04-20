from acne_detection import AcneDetector
from age_gender_estimation import AgeGenderEstimator
from dark_eye_detection import DarkEyeDetector
from facial_landmark import FacialLandmark
from wrinkles_detection import WrinklesDetector
from recommendation_system import ProductRecommendation
from sallowness_detection import get_sallowness_score
from main import SkinCareAdvisor
from os.path import join
import pandas as pd
import config
import json
import random
import time
import imutils
import cv2
from flask import Flask, request, send_file
import base64
import numpy as np
from PIL import Image
import io

# PLEASE SET THINGS IN CONFIG.PY
PRODUCT_CATALOGUE_CSV_PATH = config.PRODUCT_CATALOGUE_CSV_PATH
WEB_DIR = config.WEB_DIR
WEB_ADDRESS = config.WEB_ADDRESS
MAIN_IMAGE_WIDTH = config.MAIN_IMAGE_WIDTH
SCORE_STANDARD = config.SCORE_STANDARD
MAX_ACNE_SCORE = config.MAX_ACNE_SCORE
MAX_WRINKLES_SCORE = config.MAX_WRINKLES_SCORE
MAX_CROWS_FEET_SCORE = config.MAX_CROWS_FEET_SCORE
MAX_DARK_EYE_SCORE = config.MAX_DARK_EYE_SCORE
MAX_SALLOWNESS_SCORE = config.MAX_SALLOWNESS_SCORE
EACH_ISSUE_N_RECOMM = config.EACH_ISSUE_N_RECOMM
FULL_N_RECOMM = config.FULL_N_RECOMM


def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))


def toRGB(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)


application = Flask(__name__)


@application.route('/')
def index():
    return 'Server is running!'


@application.route('/sca', methods=['POST'])
def skincare_advice():
    user_input = request.get_json()
    img_string = user_input['image']
    image = toRGB(stringToImage(img_string))

    sca = SkinCareAdvisor(user_input, image)

    identifier = str(sca.identifier)
    url = "http://bfc7b37d.ngrok.io/image?file="

    return {
        'statusCode': 200,
        'body': {
            'full_image': url + identifier + '_full_image.jpg',
            'full_recommendations': sca.full_recommendations,
            'acne': {
                'score': {
                    'overall': sca.acne_overall,
                    'fh': sca.acne_fh,
                    'rc': sca.acne_rc,
                    'lc': sca.acne_lc,
                    'ch': sca.acne_ch
                },
                "image": {
                    "overall": url + identifier + '_full_image.jpg'
                },
                'recommendation': sca.acne_recommendation
            },
            'wrinkles': {
                'score': {
                    'overall': sca.wrinkles_overall,
                    'fh': sca.wrinkles_fh,
                    'rnl': sca.wrinkles_rnl,
                    'lnl': sca.wrinkles_lnl,
                    'rbe': sca.wrinkles_rbe,
                    'lbe': sca.wrinkles_lbe
                },
                "image": {
                    "fh": url + identifier + '_wrinkles_fh_image.jpg',
                    "rnl": url + identifier + '_wrinkles_rnl_image.jpg',
                    "lnl": url + identifier + '_wrinkles_lnl_image.jpg',
                    "rbe": url + identifier + '_wrinkles_rbe_image.jpg',
                    "lbe": url + identifier + '_wrinkles_lbe_image.jpg'
                },
            },
            'crows_feet': {
                'score': {
                    'overall': sca.crows_feet_overall,
                    'r': sca.crows_feet_r,
                    'l': sca.crows_feet_l
                },
                "image": {
                    "r": url + identifier + '_crows_feet_r_image.jpg',
                    "l": url + identifier + '_crows_feet_l_image.jpg'
                },
                'recommendation': sca.crows_feet_recommendation
            },
            'dark_eye': {
                'score': {
                    'overall': sca.dark_eye_overall
                },
                'recommendation': sca.dark_eye_recommendation
            },
            'sallowness': {
                'score': {
                    'overall': sca.sallowness_overall,
                },
                'recommendation': sca.sallowness_recommendation
            }
        }
    }


@application.route('/image')
def get_image():
    filename = request.args.get('file')
    path = './web_dir_test/' + filename
    return send_file(path, mimetype='image/gif')


if __name__ == '__main__':
    application.run(debug=False)

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
from flask import Flask, request
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

    return {
        'statusCode': 200,
        'body': {
            'identifier': sca.identifier,
            'acne_overall': sca.acne_overall,
            'acne_fh': sca.acne_fh,
            'acne_rc': sca.acne_rc,
            'acne_lc': sca.acne_lc,
            'acne_ch': sca.acne_ch,
            'wrinkles_overall': sca.wrinkles_overall,
            'wrinkles_fh': sca.wrinkles_fh,
            'wrinkles_rnl': sca.wrinkles_rnl,
            'wrinkles_lnl': sca.wrinkles_lnl,
            'wrinkles_rbe': sca.wrinkles_rbe,
            'wrinkles_lbe': sca.wrinkles_lbe,
            'crows_feet_overall': sca.crows_feet_overall,
            'crows_feet_r': sca.crows_feet_r,
            'crows_feet_l': sca.crows_feet_l,
            'dark_eye_overall': sca.dark_eye_overall,
            'sallowness_overall': sca.sallowness_overall,
            'full_recommendation': sca.full_recommendations,
            'acne_recommendation': sca.acne_recommendation,
            'wrinkles_recommendation': sca.wrinkles_recommendation,
            'crows_feet_recommendation': sca.crows_feet_recommendation,
            'dark_eye_recommendation': sca.dark_eye_recommendation,
            'sallowness_recommendation': sca.sallowness_recommendation
        }
    }


@application.route('/image', methods=['POST'])
def get_image():
    user_input = request.get_json()
    identifier = user_input['identifier']
    image_type = user_input['type']

    path = WEB_DIR + '/' + str(identifier) + '_' + image_type + '_image.jpg'

    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

        return {
            'statusCode': 200,
            'image': encoded_string.decode('utf-8')
        }


if __name__ == '__main__':
    application.run(debug=False)

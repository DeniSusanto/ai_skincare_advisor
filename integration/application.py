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
import pickle

#major integration
import dlib
from wide_resnet import WideResNet
import os
from cntk import load_model, combine

#prod_cat
PRODUCT_CATALOGUE_CSV_PATH = config.PRODUCT_CATALOGUE_CSV_PATH
prod_cat = pd.read_csv(PRODUCT_CATALOGUE_CSV_PATH)

#facial_landmark
F_L_PREDICTOR_PATH = config.F_L_PREDICTOR_PATH
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(F_L_PREDICTOR_PATH)

#age_gender
A_G_MODEL_PATH = config.A_G_MODEL_PATH
ag_model = WideResNet(64)()
ag_model.load_weights(A_G_MODEL_PATH)

#dark_eye
D_E_MODEL_PATH = config.D_E_MODEL_PATH
with open(D_E_MODEL_PATH, 'rb') as f:
    de_model = pickle.load(f)

#acne
ACNE_PRETRAINED_MODEL_NAME = config.ACNE_PRETRAINED_MODEL_NAME
ACNE_PRETRAINED_MODEL_PATH = config.ACNE_PRETRAINED_MODEL_PATH
ACNE_PRETRAINED_NODE_NAME = config.ACNE_PRETRAINED_NODE_NAME
ACNE_REGRESSION_MODEL_PATH = config.ACNE_REGRESSION_MODEL_PATH
model_file  = os.path.join(ACNE_PRETRAINED_MODEL_PATH, ACNE_PRETRAINED_MODEL_NAME)
ac_loaded_model  = load_model(model_file)
node_in_graph = ac_loaded_model.find_by_name(ACNE_PRETRAINED_NODE_NAME)
ac_output_nodes  = combine([node_in_graph.owner])
read_model = pd.read_pickle(ACNE_REGRESSION_MODEL_PATH)
regression_model = read_model['model'][0]
ac_train_regression = pickle.loads(regression_model)

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


app = Flask(__name__)


@app.route('/')
def index():
    return 'Server is running!'


@app.route('/sca', methods=['POST'])
def skincare_advice():
    img_string = request.form['image']
    image = toRGB(stringToImage(img_string))
    questionnaire = json.loads(request.form['questionnaire'])
    sca = SkinCareAdvisor(questionnaire, image, detector, predictor, prod_cat, ag_model, de_model, ac_loaded_model, ac_output_nodes, ac_train_regression)

    identifier = str(sca.identifier)
    url = "http://10.0.2.2:5000/image?file="

    return {
        'statusCode': 200,
        'body': {
            'full_image': url + identifier + '_full_image.jpg',
            'full_recommendations': sca.full_recommendations,
            'issues': {
                'Acne': {
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
                'Wrinkles': {
                    'score': {
                        'overall': sca.wrinkles_overall,
                        'fh': sca.wrinkles_fh,
                        'rnl': sca.wrinkles_rnl,
                        'lnl': sca.wrinkles_lnl,
                        'rbe': sca.wrinkles_rbe,
                        'lbe': sca.wrinkles_lbe
                    },
                    'recommendation': sca.wrinkles_recommendation
                },
                "Crow's Feet": {
                    'score': {
                        'overall': sca.crows_feet_overall,
                        'r': sca.crows_feet_r,
                        'l': sca.crows_feet_l
                    },
                    'recommendation': sca.crows_feet_recommendation
                },
                'Dark Eye Circle': {
                    'score': {
                        'overall': sca.dark_eye_overall
                    },
                    'recommendation': sca.dark_eye_recommendation
                },
                'Sallowness': {
                    'score': {
                        'overall': sca.sallowness_overall,
                    },
                    'recommendation': sca.sallowness_recommendation
                }
            },
            'concerns': sca.concerns
        }
    }


@app.route('/image')
def get_image():
    filename = request.args.get('file')
    path = './web_dir/' + filename
    return send_file(path, mimetype='image/gif')


if __name__ == '__main__':
    app.run(debug=False)

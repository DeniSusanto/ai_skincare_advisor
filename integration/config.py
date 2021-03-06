__author__ = 'Deni Susanto'
__copyright__ = 'Copyright 2020, AI Facial Skincare Advisor'
__credits__ = ['Dr. Carmen L.', 'Subhayan R.', 'Kevin H.', 'Mohammad A.']
__email__ = 'densus@hku.hk'

import numpy as np

#MAIN
PRODUCT_CATALOGUE_CSV_PATH = './product_catalogue_with_image_link.csv'
WEB_DIR = "./web_dir" #the directory to save processed images
WEB_ADDRESS = "http://139.162.62.89:5000/image?file=" #HTTP prefix to find the get the image
MAIN_IMAGE_WIDTH = 200
SCORE_STANDARD = 4
MAX_ACNE_SCORE = 4
MAX_WRINKLES_SCORE = 4
MAX_CROWS_FEET_SCORE = 4
MAX_DARK_EYE_SCORE = 2
MAX_SALLOWNESS_SCORE = 2
EACH_ISSUE_N_RECOMM = 5
FULL_N_RECOMM = 15

#facial landmark
F_L_PREDICTOR_PATH = "./models/shape_predictor_68_face_landmarks.dat"
FL_WIDTH_RESIZE = 500

#age gender estimator
A_G_MODEL_PATH = "./models/weights.28-3.73.hdf5"
MARGIN = 0.45

#acne detection
ACNE_PRETRAINED_MODEL_PATH = './models'
ACNE_PRETRAINED_MODEL_NAME = 'ResNet152_ImageNet_Caffe.model'
ACNE_PRETRAINED_NODE_NAME = 'pool5'
ACNE_REGRESSION_MODEL_PATH = './models/cntk_regression.dat'
ACNE_IMAGE_HEIGHT = 224
ACNE_IMAGE_WIDTH  = 224

#skin tone estimator
HSV_MAX = 170
YCRCB_MIN_1 = 130 
YCRCB_MAX_1 = 170
YCRCB_MIN_2 = 90
YCRCB_MAX_2 = 130

#dark eye detection
H_SPLIT_COEFF = 4
W_SPLIT_COEFF = 6
N_TOP_SELECT = int(round(0.25*(H_SPLIT_COEFF * W_SPLIT_COEFF)))
D_E_MODEL_PATH = "./models/dark_eye_detection_model.pickle"

#wrinkles detection
HESSIAN_SIGMA = 12.0
GAUSSIAN_KERNEL_SIZE = 41
CANNY_LOW_THRESHOLD = 25
CANNY_HIGH_THRESHOLD = 35
HOUGH_RHO = 10
HOUGH_THRESHOLD = 15
HOUGH_THETA = np.pi/180
HOUGH_MIN_LINE_LENGTH = 100
HOUGH_MAX_LINE_GAP = 1
CLIP_LIMIT = 3.0
TILE_GRID_SIZE = (8,8)

HESSIAN_CROWS_FEET_CROP = 0.06
HESSIAN_FOREHEAD_CROP = 0.08
HESSIAN_BELOW_EYES_CROP = 0.07
HESSIAN_NASAL_LINES_CROP = 0.10

CROWS_FEET_WIDTH = 300
FOREHEAD_WIDTH = 1000
BELOW_EYES_WIDTH = 350
NASAL_LINES_WIDTH = 250

CROWS_FEET_THRESHOLD = (10, 25, 45, 70, 90)
FOREHEAD_THRESHOLD = (10, 25, 45, 60, 80)
BELOW_EYES_THRESHOLD = (10, 25, 45, 70, 90)
NASAL_LINES_THRESHOLD = (10, 15, 40, 60, 80)

FH_WEIGHT = 0.45
BE_WEIGHT = 0.10
CF_WEIGHT = 0.20
NL_WEIGHT = 0.25

#RECOMMENDATION SYSTEM
FACIAL_ISSUES_KEYS = ['acne', 'wrinkles', 'crows_feet', 'dark_eye', 'sallowness', 'dryness']
AVAILABLE_CONCERNS = ['dryness', 'wrinkles', 'oiliness', 'dullness', 'dark_spots', 'pores', 'redness', 'acne', 'uneven_skin_tone', 'sallowness']
CONCERNS_NAME_MAPPING = {
'dryness' : "Dryness", 'wrinkles' : "Wrinkles", 'oiliness' : "Oiliness", 'dullness': "Dullness", 'dark_spots': "Dark Spots", 'pores': "Pores", 'redness': "Redness", 'acne': "Acne", 'uneven_skin_tone': "Uneven Skin Tone", 'sallowness': "Sallowness"
}
PRODUCT_CATALOGUE_PATH = "product_catalogue.csv"
RECOMMENDATION_THRESHOLD = {
    'acne' : 1.5, 
    'wrinkles' : 1.5, 
    'crows_feet' : 1.5, 
    'dark_eye' : 0.7, 
    'sallowness' : 1.0
}
RECOMMENDATION_PRODUCT_MAPPING = {
    'acne' : ['Cleanser'],
    'wrinkles' : ['Treatment'], 
    'crows_feet' : ['Treatment'], 
    'dark_eye' : ['Eye cream'], 
    'sallowness' : ['Face Mask'],
    'dryness' : ['Moisturizer']
}

RS_PRICE_WEIGHT = 0.2
RS_RATINGS_WEIGHT = 0.25
RS_LIKES_WEIGHT = 0.35
RS_PREFERENCES_WEIGHT = 0.2
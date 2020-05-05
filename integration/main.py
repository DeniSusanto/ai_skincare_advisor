from acne_detection import AcneDetector
from age_gender_estimation import AgeGenderEstimator
from dark_eye_detection import DarkEyeDetector
from facial_landmark import FacialLandmark
from wrinkles_detection import WrinklesDetector
from recommendation_system import ProductRecommendation
from sallowness_detection import get_sallowness_score
from os.path import join
import pandas as pd
import numpy as np
import config
import json
import random
import time
import imutils
import cv2
import numpy as np

#PLEASE SET THINGS IN CONFIG.PY
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
ISSUES_LIST = config.FACIAL_ISSUES_KEYS
CONCERNS_NAME_MAPPING = config.CONCERNS_NAME_MAPPING
AVAILABLE_CONCERNS = config.AVAILABLE_CONCERNS
def standardize_score(score, from_standard, to_standard = SCORE_STANDARD):
    return (score/from_standard)*to_standard

#this function might need modification depending on the server setup
def saveImage(image, file_name, prefix,  directory = WEB_DIR, address = WEB_ADDRESS):
    rev_file_name = str(prefix) + "_" + file_name
    path = join(directory, rev_file_name)
    cv2.imwrite(path, image)
    
    return WEB_ADDRESS + rev_file_name

#identifier is a parameter that will appended to the processed images to differentiate between users. If unique_id is None, then the program will generate random ID
#questionnaire is string in json format
#image is an OPENCV2 IMAGE OBJECT from CV2.imread('path'). Since the cv2.imread behavior is to read image in "BGR" format, then pls read the image using opencv2 in the API code.

#questionnaire should have these keys: age, skin_type, allergies, price, concerns, preferences 
class SkinCareAdvisor():
    def __init__(self, questionnaire, image, detector, predictor, prod_cat, ag_model, de_model, ac_loaded_model, ac_output_nodes, ac_train_regression, identifier=None):
        if not identifier:
            identifier = random.getrandbits(64)
        self.identifier = identifier
        self.prod_cat = prod_cat
        facial_landmark = FacialLandmark(image, detector, predictor)
        
        age_gender = AgeGenderEstimator(facial_landmark, ag_model)
        dark_eyes = DarkEyeDetector(facial_landmark, de_model)
        acne = AcneDetector(facial_landmark, ac_loaded_model, ac_output_nodes, ac_train_regression)
        wrinkles = WrinklesDetector(facial_landmark)
        wrinkles.complete_init()
        
        #Take care of scoring matters first
        #acne
        acne_overall = acne.get_overall_score()
        self.acne_overall = standardize_score(acne_overall, MAX_ACNE_SCORE)
        self.acne_fh = standardize_score(acne.get_forehead_score(), MAX_ACNE_SCORE)
        acne_cheek_score = acne.get_cheeks_score()
        self.acne_rc = standardize_score(acne_cheek_score[0], MAX_ACNE_SCORE)
        self.acne_lc = standardize_score(acne_cheek_score[1], MAX_ACNE_SCORE)
        self.acne_ch = standardize_score(acne.get_chin_score(), MAX_ACNE_SCORE)
        acne_adjusted_score = np.max([self.acne_overall, self.acne_rc, self.acne_lc, self.acne_ch])
        
        #wrinkles
        wrinkles_overall = wrinkles.overall_score
        self.wrinkles_overall = standardize_score(wrinkles_overall, MAX_WRINKLES_SCORE)
        self.wrinkles_fh = standardize_score(wrinkles.fh_score, MAX_WRINKLES_SCORE)
        self.wrinkles_rnl = standardize_score(wrinkles.r_nl_score, MAX_WRINKLES_SCORE)
        self.wrinkles_lnl = standardize_score(wrinkles.l_nl_score, MAX_WRINKLES_SCORE)
        self.wrinkles_rbe = standardize_score(wrinkles.r_be_score, MAX_WRINKLES_SCORE)
        self.wrinkles_lbe = standardize_score(wrinkles.l_be_score, MAX_WRINKLES_SCORE)
        wrinkles_adjusted_score = np.max([self.wrinkles_overall, self.wrinkles_fh, self.wrinkles_rnl, self.wrinkles_lnl, self.wrinkles_rbe, self.wrinkles_lbe])
        
        #crows feet
        crows_feet_overall = wrinkles.cf_score
        self.crows_feet_overall = standardize_score(crows_feet_overall, MAX_CROWS_FEET_SCORE)
        self.crows_feet_r = standardize_score(wrinkles.r_cf_score, MAX_CROWS_FEET_SCORE)
        self.crows_feet_l = standardize_score(wrinkles.l_cf_score, MAX_CROWS_FEET_SCORE)
        
        #dark_eye
        dark_eye_overall = dark_eyes.get_score()
        self.dark_eye_overall = standardize_score(dark_eye_overall, MAX_DARK_EYE_SCORE)
        
        #sallowness
        if questionnaire["age"]:
            real_age = int(questionnaire["age"])
        else:
            real_age = 100
        predicted_age = age_gender.predict_age_gender()[0]
        sallowness_overall = get_sallowness_score(real_age,predicted_age)
        self.sallowness_overall = standardize_score(sallowness_overall, MAX_SALLOWNESS_SCORE)
        
        
        #Take care of the images
        resized_image = imutils.resize(image, width=MAIN_IMAGE_WIDTH)
        self.full_image = saveImage(resized_image, "full_image.jpg", self.identifier)
        
        #wrinkles
#         self.wrinkles_fh_image = saveImage(wrinkles.fh_image, "wrinkles_fh_image.jpg", self.identifier)
#         self.wrinkles_rnl_image = saveImage(wrinkles.r_nl_image, "wrinkles_rnl_image.jpg", self.identifier)
#         self.wrinkles_lnl_image = saveImage(wrinkles.l_nl_image, "wrinkles_lnl_image.jpg", self.identifier)
#         self.wrinkles_rbe_image = saveImage(wrinkles.r_be_image, "wrinkles_rbe_image.jpg", self.identifier)
#         self.wrinkles_lbe_image = saveImage(wrinkles.l_be_image, "wrinkles_lbe_image.jpg", self.identifier)
        
#         #crows_feet
#         self.crows_feet_r_image = saveImage(wrinkles.r_cf_image, "crows_feet_r_image.jpg", self.identifier)
#         self.crows_feet_l_image = saveImage(wrinkles.l_cf_image, "crows_feet_l_image.jpg", self.identifier)
        
        #Take care of the recommendation
        allergy = None if questionnaire['allergies']=="" else questionnaire['allergies'].lower().replace(" ", "").split(",")
        pref = None if questionnaire['preferences']=="" else questionnaire['preferences'].lower().replace(" ", "").split(",")
        main_input = {
            'acne': acne_adjusted_score,
            'wrinkles': wrinkles_adjusted_score,
            'crows_feet': crows_feet_overall,
            'dark_eye': dark_eye_overall,
            'sallowness': sallowness_overall,
            'skin_type': questionnaire['skin_type'],
            'allergies': allergy,
            'price': questionnaire['price'],
            'concerns': questionnaire['concerns'],
            'preferences': pref
        }
        prod_rec = ProductRecommendation(self.prod_cat, main_input)
        recom_object = prod_rec.get_default_recommendation()
        
        #full_recom
        full_recommendations = {}
        if 'all_products' in recom_object:
            recom_df = recom_object['all_products']
            counter = 0
            for idx, row in recom_df.iterrows():
                if FULL_N_RECOMM == counter:
                    break
                full_recommendations[idx] = {
                    "title":row['name'],
                    "issue": row['Label'],
                    "image":{
                        "uri": row['image_url']
                    },
                    "price":row['price'],
                    "rating":row['rating'],
                    "likes":row['likes'],
                    "description":row['description'],
                }
                counter += 1
        self.full_recommendations = json.dumps(full_recommendations)
        
        
        #Acne
        self.acne_recommendation = self._get_recom_json(recom_object, 'acne','Cleanser', 'Acne')
        #Wrinkles
        self.wrinkles_recommendation = self._get_recom_json(recom_object, 'wrinkles', 'Treatment', 'Wrinkles')
        #crows_feet
        self.crows_feet_recommendation = self._get_recom_json(recom_object, 'crows_feet','Treatment', "Crow's Feet")
        #dark_eye
        self.dark_eye_recommendation = self._get_recom_json(recom_object, 'dark_eye','Eye cream', 'Dark Eye Circle')
        #sallowness
        self.sallowness_recommendation = self._get_recom_json(recom_object, 'sallowness','Face Mask', 'Sallowness')
        
        #taking care of concern
        self.concerns = self._extract_concerns_json(recom_object)
        
    def _get_recom_json(self, recom_object, key, label, issue_name, limit=EACH_ISSUE_N_RECOMM):
        tmp = {}
        if key in recom_object:
            if label:
                recom_df = recom_object[key][label]
            else:
                recom_df = recom_object[key]
            counter = 0
            for idx, row in recom_df.iterrows():
                if limit == counter:
                    break
                tmp[idx] = {
                    "title":row['name'],
                    "issue": issue_name,
                    "image":{
                        "uri": row['image_url']
                    },
                    "price":row['price'],
                    "rating":row['rating'],
                    "likes":row['likes'],
                    "description":row['description'],
                }
                counter += 1
        return json.dumps(tmp)
    
    def _extract_concerns_json(self, recom_object):
        tmp = {}
        for key in recom_object:
            if (key not in ISSUES_LIST) and (key in AVAILABLE_CONCERNS):
                concern_name = CONCERNS_NAME_MAPPING[key]
                tmp[concern_name] = {}
                tmp[concern_name]["recommendation"] = {}
                recom_df = recom_object[key]
                counter = 0
                for idx, row in recom_df.iterrows():
                    if EACH_ISSUE_N_RECOMM == counter:
                        break
                    tmp[concern_name]["recommendation"][idx] = {
                        "title":row['name'],
                        "issue": concern_name,
                        "image":{
                            "uri": row['image_url']
                        },
                        "price":row['price'],
                        "rating":row['rating'],
                        "likes":row['likes'],
                        "description":row['description'],
                    }
                    counter += 1
        return json.dumps(tmp)
import numpy as np
import cv2
import os
import pandas as pd
import pickle
from cntk import load_model, combine
import config

#config variables
ACNE_PRETRAINED_MODEL_NAME = config.ACNE_PRETRAINED_MODEL_NAME
ACNE_PRETRAINED_MODEL_PATH = config.ACNE_PRETRAINED_MODEL_PATH
ACNE_PRETRAINED_NODE_NAME = config.ACNE_PRETRAINED_NODE_NAME
ACNE_REGRESSION_MODEL_PATH = config.ACNE_REGRESSION_MODEL_PATH
ACNE_IMAGE_HEIGHT = config.ACNE_IMAGE_HEIGHT
ACNE_IMAGE_WIDTH  = config.ACNE_IMAGE_WIDTH

#a class for detecting acne
class AcneDetector():
    def __init__(self, facial_landmark):
        self.facial_landmark = facial_landmark
        self.image = facial_landmark.image.copy()
        model_file  = os.path.join(ACNE_PRETRAINED_MODEL_PATH, ACNE_PRETRAINED_MODEL_NAME)
        self.loaded_model  = load_model(model_file)
        node_in_graph = self.loaded_model.find_by_name(ACNE_PRETRAINED_NODE_NAME)
        self.output_nodes  = combine([node_in_graph.owner])

        read_model = pd.read_pickle(ACNE_REGRESSION_MODEL_PATH)
        regression_model = read_model['model'][0]
        self.train_regression = pickle.loads(regression_model)
        
        fh_region = self.facial_landmark.get_forehead_region()
        fh_score = self._predict_score(fh_region)
        self._fh_score = fh_score
        
        ch_region = self.facial_landmark.get_chin_region()
        ch_score = self._predict_score(ch_region)
        self._ch_score = ch_score
        
        rc_region, lc_region = self.facial_landmark.get_cheeks_region()
        rc_score = self._predict_score(rc_region)
        lc_score = self._predict_score(lc_region)
        self._rc_score = rc_score
        self._lc_score = lc_score
    
    #extract image features from RESNET pretrained model
    #return features
    def _extract_features(self, image):   
        image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(image_RGB, (ACNE_IMAGE_WIDTH, ACNE_IMAGE_HEIGHT), interpolation = cv2.INTER_AREA)
        bgr_image = np.asarray(resized, dtype=np.float32)[..., [2, 1, 0]]    
        hwc_format = np.ascontiguousarray(np.rollaxis(bgr_image, 2)) 

        arguments = {self.loaded_model.arguments[0]: [hwc_format]}    
        output = self.output_nodes.eval(arguments)   
        return output
    
    #predict score of an image using the features extracted from RESNET and use those features to predict score from the trained MLP model
    #return score
    def _predict_score(self, image):
        score_features = self._extract_features(image)[0].flatten()
        pred_score_label = self.train_regression.predict(score_features.reshape(1,-1))
        score = float("{0:.3f}".format(pred_score_label[0]))
        adjusted_score = score - 1
        return adjusted_score
    
    def get_forehead_score(self):
        return self._fh_score
    
    def get_chin_score(self):
        return ch_score
    
    #return (right cheek score, left cheek score) tuple
    def get_cheeks_score(self):
        return (self._rc_score, self._lc_score)
    
    #return avg score
    def get_overall_score(self):
        scores = np.asarray([self._fh_score, self._ch_score, self._rc_score, self._lc_score])
        avg_score = float("{0:.3f}".format(np.mean(scores)))
        return avg_score
        
            
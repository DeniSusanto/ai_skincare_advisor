import imutils
import numpy as np
import cv2
import tensorflow as tf
import config


MARGIN = config.MARGIN

class AgeGenderEstimator():
    def __init__(self, facial_landmark, model):
        self.model = model
        self.facial_landmark = facial_landmark
        self.image = facial_landmark.image.copy()
    
    #return (age prediction, gender), gender can be "M" or "F"
    def predict_age_gender(self):
        img_h, img_w, _ = np.shape(self.image)
        facial_landmark = self.facial_landmark
        
        w = facial_landmark.bb_x2 - facial_landmark.bb_x1
        h = facial_landmark.bb_y2 - facial_landmark.bb_y1
        
        xw1 = max(int(facial_landmark.bb_x1 - MARGIN * w), 0)
        yw1 = max(int(facial_landmark.bb_y1 - MARGIN * h), 0)
        xw2 = min(int(facial_landmark.bb_x2 + MARGIN * w), img_w - 1)
        yw2 = min(int(facial_landmark.bb_y2 + MARGIN * h), img_h - 1)
        
        face = np.asarray([cv2.resize(self.image[yw1:yw2 + 1, xw1:xw2 + 1, :], (64, 64))])
        
        result = self.model.predict(face)
        predicted_gender = "M" if result[0][0][0] < 0.5 else "F"
        
        ages = np.arange(0, 101).reshape(101, 1)
        predicted_age = int(round(result[1].dot(ages).flatten()[0]))
           
        return (predicted_age, predicted_gender)

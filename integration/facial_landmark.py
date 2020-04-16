__author__ = 'Deni Susanto'
__copyright__ = 'Copyright 2020, AI Facial Skincare Advisor'
__credits__ = ['Dr. Carmen L.', 'Subhayan R.', 'Kevin H.', 'Mohammad A.']
__email__ = 'densus@hku.hk'

import dlib
import imutils
from imutils import face_utils
import cv2
import numpy as np
import config

F_L_PREDICTOR_PATH = config.F_L_PREDICTOR_PATH
FL_WIDTH_RESIZE = config.FL_WIDTH_RESIZE

class FacialLandmark():
    def __init__(self, image):
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(F_L_PREDICTOR_PATH)
        
        (ori_height, ori_width) = image.shape[:2]
        resized_image = imutils.resize(image, width=FL_WIDTH_RESIZE)
        (trans_height, trans_width) = resized_image.shape[:2]
        
        ratio_x = ori_width/trans_width
        ratio_y = ori_height/trans_height
        
        gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)
        rect = rects[0]
        shape = predictor(gray, rect)
        landmark = face_utils.shape_to_np(shape)
        adjusted_landmark = [(int(round(x * ratio_x)), int(round(y * ratio_y))) for (x,y) in landmark]
        adjusted_landmark = np.asarray(adjusted_landmark)
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        
        self.image = image
        self.resized_image = resized_image
        self.landmark = adjusted_landmark
        self.bb_x1 = int(round(x * ratio_x))
        self.bb_y1 = int(round(y * ratio_y))
        self.bb_x2 = int(round((x + w) * ratio_x))
        self.bb_y2 = int(round((y + h) * ratio_y))
    
    def _returnImage(self, x1, x2, y1, y2, highLight):
        if not highLight:
            return self.image[y1:y2, x1:x2]
        else:
            img_copy = self.image.copy()
            cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 1)
            return img_copy
    
    def get_below_eyes_region(self, highlight = False, coor = False):
        right_eye_h = round(1.2*(self.landmark[41][1] - self.landmark[37][1]))
        left_eye_h = round(1.2*(self.landmark[46][1] - self.landmark[44][1]))
        right_eye_lp = int(max(self.landmark[41][1], self.landmark[40][1]) + 0.5 * right_eye_h)
        left_eye_lp = int(max(self.landmark[46][1], self.landmark[47][1]) + 0.5 * left_eye_h)
        
        r_x1 = self.landmark[36][0] - int(0.15 * (self.landmark[36][0] - self.landmark[0][0]))
        r_x2 = self.landmark[39][0]
        r_y1 = right_eye_lp
        r_y2 = right_eye_lp + int(1.2 * right_eye_h)
        
        l_x1 = self.landmark[42][0]
        l_x2 = self.landmark[45][0] + int(0.15 * (self.landmark[16][0] - self.landmark[45][0]))
        l_y1 = left_eye_lp
        l_y2 = left_eye_lp + int(1.2 * left_eye_h)
        
        if coor:
            return ((self._returnImage(r_x1, r_x2, r_y1, r_y2, highlight), (r_x1, r_x2, r_y1, r_y2) ), (self._returnImage(l_x1, l_x2, l_y1, l_y2, highlight), (l_x1, l_x2, l_y1, l_y2)))
        
        return (self._returnImage(r_x1, r_x2, r_y1, r_y2, highlight), self._returnImage(l_x1, l_x2, l_y1, l_y2, highlight))
    
    def get_crows_feet_region(self, highlight = False, coor = False):
        right_cf_w = self.landmark[36][0] - self.landmark[0][0]
        left_cf_w = self.landmark[16][0] - self.landmark[45][0]
        right_cf_h = self.landmark[36][1] - self.landmark[17][1]
        left_cf_h = self.landmark[45][1] - self.landmark[26][1]
        r_w_portion = int(0.1 * right_cf_w)
        l_w_portion = int(0.1 * left_cf_w)
        r_h_portion = int(0.85 * right_cf_h)
        l_h_portion = int(0.85 * left_cf_h)
        r_x1 = self.landmark[0][0] + r_w_portion
        r_x2 = self.landmark[36][0] - 3*r_w_portion
        r_y1 = self.landmark[36][1] - r_h_portion
        r_y2 = self.landmark[36][1] + round(1.5*r_h_portion)
        
        l_x1 = self.landmark[45][0] + 3*l_w_portion
        l_x2 = self.landmark[16][0] - l_w_portion
        l_y1 = self.landmark[45][1] - r_h_portion
        l_y2 = self.landmark[45][1] + round(1.5*r_h_portion)
        
        if coor:
            return ((self._returnImage(r_x1, r_x2, r_y1, r_y2, highlight), (r_x1, r_x2, r_y1, r_y2) ), (self._returnImage(l_x1, l_x2, l_y1, l_y2, highlight), (l_x1, l_x2, l_y1, l_y2)))
        
        return (self._returnImage(r_x1, r_x2, r_y1, r_y2, highlight), self._returnImage(l_x1, l_x2, l_y1, l_y2, highlight))
    
    def get_forehead_region(self, highlight = False, coor = False):
        face_y_min = int((min(self.landmark[:,1]).flatten()[0]))
        face_y_max = int(np.asarray(max(self.landmark[:,1]).flatten()[0]))
        face_height = face_y_max - face_y_min 
        forehead_height = int(face_height * 0.25)
        
        x1 = self.landmark[37][0]
        x2 = self.landmark[44][0]
        y1 = face_y_min - forehead_height
        y2 = face_y_min
        
        if coor:
            return (self._returnImage(x1, x2, y1, y2, highlight), (x1, x2, y1, y2))
            
        return self._returnImage(x1, x2, y1, y2, highlight)
    
    def get_nasal_junction_region(self, highlight = False, coor = False):
        r_lips = self.landmark[61][1] - self.landmark[50][1]
        r_nose_alare = self.landmark[33][0] - self.landmark[31][0]
        r_x1 = self.landmark[36][0]
        r_x2 = self.landmark[31][0] - int(0.2 * r_nose_alare)
        r_y1 = self.landmark[30][1]
        r_y2 = self.landmark[48][1] - r_lips
        
        l_lips = self.landmark[63][1] - self.landmark[52][1]
        l_nose_alare = self.landmark[35][0] - self.landmark[33][0]
        l_x1 = self.landmark[35][0] + int(0.2 * l_nose_alare)
        l_x2 = self.landmark[45][0]
        l_y1 = self.landmark[30][1]
        l_y2 = self.landmark[54][1] - l_lips
        
        if coor:
            return ((self._returnImage(r_x1, r_x2, r_y1, r_y2, highlight), (r_x1, r_x2, r_y1, r_y2) ), (self._returnImage(l_x1, l_x2, l_y1, l_y2, highlight), (l_x1, l_x2, l_y1, l_y2)))
        
        return (self._returnImage(r_x1, r_x2, r_y1, r_y2, highlight), self._returnImage(l_x1, l_x2, l_y1, l_y2, highlight))
    
    def get_chin_region(self, highlight = False, coor = False):
        chin_x_min = self.landmark[39][0]
        chin_x_max = self.landmark[42][0]
        mouse_landmarks = self.landmark[list(range(48, 61)),:]
        chin_y_min = np.max(np.array(mouse_landmarks[:,1]))
        chin_y_max = int(np.asarray(max(self.landmark[:,1]).flatten()[0]))
        
        h = chin_y_max - chin_y_min
        x1 = chin_x_min
        x2 = chin_x_max
        y1 = chin_y_min + int(0.05 * h)
        y2 = chin_y_max - int(0.10 * h)
        
        if coor:
            return (self._returnImage(x1, x2, y1, y2, highlight), (x1, x2, y1, y2))
        
        return self._returnImage(x1, x2, y1, y2, highlight)
    
    def get_cheeks_region(self, highlight = False, coor = False):
        face_x_min = int(max(0, np.asarray(min(self.landmark[:,0])).flatten()[0]))
        face_x_max = int(np.asarray(max(self.landmark[:,0])).flatten()[0])
        face_y_min = int((min(self.landmark[:,1]).flatten()[0]))
        face_y_max = int(np.asarray(max(self.landmark[:,1]).flatten()[0]))
        
        r_cheek_min_x = int(face_x_min + 0.05 * (self.landmark[39][0] - face_x_min))
        r_cheek_max_x = max(self.landmark[39][0], self.landmark[31][0])
        l_cheek_min_x = min(self.landmark[42][0], self.landmark[35][0])
        l_cheek_max_x = int(face_x_max - 0.05 * (face_x_max - self.landmark[42][0]))
        
        r_eye_landmarks = self.landmark[list(range(36, 42)),:]
        l_eye_landmarks = self.landmark[list(range(42, 48)),:]
        
        r_cheek_min_y = int(max(r_eye_landmarks[:,1]) + 0.2 * (max(r_eye_landmarks[:,1]) - min(r_eye_landmarks[:,1])))
        r_cheek_max_y = int(face_y_max - 0.1 * (face_y_max - max(r_eye_landmarks[:,1])))
        l_cheek_min_y = int(max(l_eye_landmarks[:,1]) + 0.2 * (max(l_eye_landmarks[:,1])  - min(l_eye_landmarks[:,1])))
        l_cheek_max_y = int(face_y_max - 0.1 * (face_y_max - max(l_eye_landmarks[:,1])))
        
        r_w = r_cheek_max_x - r_cheek_min_x
        l_w = l_cheek_max_x - l_cheek_min_x
        r_cheek_min_x = r_cheek_min_x + int(0.025 * r_w)
        r_cheek_max_x = r_cheek_max_x - int(0.1 * r_w)
        l_cheek_min_x = l_cheek_min_x + int(0.1 * l_w)
        l_cheek_max_x = l_cheek_max_x - int(0.025 * l_w)
        
        if coor:
            return ((self._returnImage(r_cheek_min_x, r_cheek_max_x, r_cheek_min_y, r_cheek_max_y, highlight), (r_cheek_min_x, r_cheek_max_x, r_cheek_min_y, r_cheek_max_y) ), (self._returnImage(l_cheek_min_x, l_cheek_max_x, l_cheek_min_y, l_cheek_max_y, highlight), (l_cheek_min_x, l_cheek_max_x, l_cheek_min_y, l_cheek_max_y)))
        
        return (self._returnImage(r_cheek_min_x, r_cheek_max_x, r_cheek_min_y, r_cheek_max_y, highlight), 
                self._returnImage(l_cheek_min_x, l_cheek_max_x, l_cheek_min_y, l_cheek_max_y, highlight))
        
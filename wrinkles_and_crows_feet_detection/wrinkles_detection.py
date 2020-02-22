__author__ = 'Deni Susanto'
__copyright__ = 'Copyright 2020, AI Facial Skincare Advisor'
__credits__ = ['Dr. Carmen L.', 'Subhayan R.', 'Kevin H.', 'Mohammad A.']
__email__ = 'densus@hku.hk'

import cv2
from skimage.feature import hessian_matrix, hessian_matrix_eigvals
import matplotlib
import matplotlib.cm as cm
import imutils
import numpy as np
import config

HESSIAN_SIGMA = config.HESSIAN_SIGMA
GAUSSIAN_KERNEL_SIZE = config.GAUSSIAN_KERNEL_SIZE
CANNY_LOW_THRESHOLD = config.CANNY_LOW_THRESHOLD
CANNY_HIGH_THRESHOLD = config.CANNY_HIGH_THRESHOLD
HOUGH_RHO = config.HOUGH_RHO
HOUGH_THRESHOLD = config.HOUGH_THRESHOLD
HOUGH_THETA = config.HOUGH_THETA
HOUGH_MIN_LINE_LENGTH = config.HOUGH_MIN_LINE_LENGTH
HOUGH_MAX_LINE_GAP = config.HOUGH_MAX_LINE_GAP
CLIP_LIMIT = config.CLIP_LIMIT
TILE_GRID_SIZE = config.TILE_GRID_SIZE

HESSIAN_CROWS_FEET_CROP = config.HESSIAN_CROWS_FEET_CROP
HESSIAN_FOREHEAD_CROP = config.HESSIAN_FOREHEAD_CROP
HESSIAN_BELOW_EYES_CROP = config.HESSIAN_BELOW_EYES_CROP
HESSIAN_NASAL_LINES_CROP = config.HESSIAN_NASAL_LINES_CROP

CROWS_FEET_WIDTH = config.CROWS_FEET_WIDTH
FOREHEAD_WIDTH = config.FOREHEAD_WIDTH
BELOW_EYES_WIDTH = config.BELOW_EYES_WIDTH
NASAL_LINES_WIDTH = config.NASAL_LINES_WIDTH

CROWS_FEET_THRESHOLD = config.CROWS_FEET_THRESHOLD
FOREHEAD_THRESHOLD = config.FOREHEAD_THRESHOLD
BELOW_EYES_THRESHOLD = config.BELOW_EYES_THRESHOLD
NASAL_LINES_THRESHOLD = config.NASAL_LINES_THRESHOLD

#Overall score weighting
FH_WEIGHT = config.FH_WEIGHT
BE_WEIGHT = config.BE_WEIGHT
CF_WEIGHT = config.CF_WEIGHT
NL_WEIGHT = config.NL_WEIGHT

def get_middle_number(a, b):
    maxim = max(a,b)
    minim = min(a,b)
    dist = (maxim - minim)/2
    return minim + dist

class WrinklesDetector():
    def __init__(self, facial_landmark):
        self.facial_landmark = facial_landmark
        self.image = facial_landmark.image
    
    def _detect_ridges(self, gray, sigma=3.0):
        elem = hessian_matrix(gray, sigma)
        i1, i2 = hessian_matrix_eigvals(elem)
        return i1, i2

    def _get_raw_score(self, image, lines):
        total = 0
        for line in lines:
            for x1,y1,x2,y2 in line:
                total += np.hypot(x2-x1, y2-y1)
        score = total / (image.shape[0] * image.shape[1] / 10000)
        return score
    
    def _score_threshold(self, raw_score, threshold):
        if raw_score < threshold[0]:
            return 0
        elif raw_score < get_middle_number(threshold[0], threshold[1]):
            return 0.5
        elif raw_score < threshold[1]:
            return 1
        elif raw_score < get_middle_number(threshold[1], threshold[2]):
            return 1.5
        elif raw_score < threshold[2]:
            return 2
        elif raw_score < get_middle_number(threshold[2], threshold[3]):
            return 2.5
        elif raw_score < threshold[3]:
            return 3
        elif raw_score < get_middle_number(threshold[3], threshold[4]):
            return 3.5
        else:
            return 4

    def _detect_wrinkle(self, input_image, crop_portion = 0, x_crop = False):
        image = input_image.copy()
        lab= cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=CLIP_LIMIT, tileGridSize=TILE_GRID_SIZE)
        cl = clahe.apply(l)
        limg = cv2.merge((cl,a,b))
        final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        image_gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
        a, b = self._detect_ridges(image_gray, sigma=HESSIAN_SIGMA)
        #rescale scalar value to RGB
        norm = matplotlib.colors.Normalize(vmin=np.min(a), vmax=np.max(a), clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=cm.Greys_r)
        conv = ((1-mapper.to_rgba(a)[:,:,0])*255).astype(np.uint8)
        if x_crop:
            image_width = image.shape[1]
            portion = round(crop_portion * image_width)
            cropped_conv =  conv[0:image.shape[0], portion:(image_width - portion)]
        else:
            image_height = image.shape[0]
            portion = round(crop_portion * image_height)
            cropped_conv =  conv[portion:(image_height - portion), 0:image.shape[1]]
        blurred = cv2.GaussianBlur(cropped_conv, (GAUSSIAN_KERNEL_SIZE, GAUSSIAN_KERNEL_SIZE), 0)
        edged = cv2.Canny(blurred, CANNY_LOW_THRESHOLD, CANNY_HIGH_THRESHOLD)
        lines = cv2.HoughLinesP(edged, HOUGH_RHO, HOUGH_THETA, HOUGH_THRESHOLD, HOUGH_MIN_LINE_LENGTH, HOUGH_MAX_LINE_GAP)
        adjusted_lines = []
        highlighted_image = input_image.copy()
        if lines is not None:
            for line in lines:
                for x1,y1,x2,y2 in line:
                    if x_crop:
                        adjusted_lines.append([(x1 + portion, y1, x2 + portion, y2)])
                        cv2.line(highlighted_image,(x1 + portion,y1),(x2 + portion,y2),(0,255,0),2)
                    else:
                        adjusted_lines.append([(x1, y1 + portion, x2, y2 + portion)])
                        cv2.line(highlighted_image,(x1,y1 + portion),(x2,y2 + portion),(0,255,0),2)
        return(highlighted_image, adjusted_lines)
    
    def get_crows_feet(self):
        crows_feet_r, crows_feet_l = self.facial_landmark.get_crows_feet_region()
        crows_feet_r = imutils.resize(crows_feet_r, width=CROWS_FEET_WIDTH)
        crows_feet_l = imutils.resize(crows_feet_l, width=CROWS_FEET_WIDTH)
        r_highlighted_image, r_adjusted_lines = self._detect_wrinkle(crows_feet_r, crop_portion = HESSIAN_CROWS_FEET_CROP)
        l_highlighted_image, l_adjusted_lines = self._detect_wrinkle(crows_feet_l, crop_portion = HESSIAN_CROWS_FEET_CROP)
        r_raw_score = self._get_raw_score(crows_feet_r, r_adjusted_lines)
        l_raw_score = self._get_raw_score(crows_feet_l, l_adjusted_lines)
        
        r_score = self._score_threshold(r_raw_score, CROWS_FEET_THRESHOLD)
        l_score = self._score_threshold(l_raw_score, CROWS_FEET_THRESHOLD)
        overall_score = self._score_threshold(np.mean([r_raw_score, l_raw_score]), CROWS_FEET_THRESHOLD)
        return ((r_highlighted_image, r_score), (l_highlighted_image, l_score), overall_score)
    
    def get_forehead(self):
        forehead_region = self.facial_landmark.get_forehead_region()
        forehead_region = imutils.resize(forehead_region, width=FOREHEAD_WIDTH)
        forehead_highlighted_image, forehead_adjusted_lines = self._detect_wrinkle(forehead_region, crop_portion = HESSIAN_FOREHEAD_CROP)
        forehead_raw_score = self._get_raw_score(forehead_region, forehead_adjusted_lines) 
        forehead_score = self._score_threshold(forehead_raw_score, FOREHEAD_THRESHOLD)
        return (forehead_highlighted_image, forehead_score)
    
    def get_below_eyes(self):
        below_eyes_r, below_eyes_l = self.facial_landmark.get_below_eyes_region()
        below_eyes_r = imutils.resize(below_eyes_r, width=BELOW_EYES_WIDTH)
        below_eyes_l = imutils.resize(below_eyes_l, width=BELOW_EYES_WIDTH)
        r_highlighted_image, r_adjusted_lines = self._detect_wrinkle(below_eyes_r, crop_portion = HESSIAN_BELOW_EYES_CROP, x_crop = True)
        l_highlighted_image, l_adjusted_lines = self._detect_wrinkle(below_eyes_l, crop_portion = HESSIAN_BELOW_EYES_CROP, x_crop = True)
        r_raw_score = self._get_raw_score(below_eyes_r, r_adjusted_lines)
        l_raw_score = self._get_raw_score(below_eyes_l, l_adjusted_lines)
        r_score = self._score_threshold(r_raw_score, BELOW_EYES_THRESHOLD)
        l_score = self._score_threshold(l_raw_score, BELOW_EYES_THRESHOLD)
        overall_score = self._score_threshold(np.mean([r_raw_score, l_raw_score]), BELOW_EYES_THRESHOLD)
        return ((r_highlighted_image, r_score), (l_highlighted_image, l_score), overall_score)
    
    def get_nasal_lines(self):
        nasal_junction_r, nasal_junction_l = self.facial_landmark.get_nasal_junction_region()
        nasal_junction_r = imutils.resize(nasal_junction_r, width=NASAL_LINES_WIDTH)
        nasal_junction_l = imutils.resize(nasal_junction_l, width=NASAL_LINES_WIDTH)
        r_highlighted_image, r_adjusted_lines = self._detect_wrinkle(nasal_junction_r, 
                                                                     crop_portion = HESSIAN_NASAL_LINES_CROP, x_crop = True)
        l_highlighted_image, l_adjusted_lines = self._detect_wrinkle(nasal_junction_l, 
                                                                     crop_portion = HESSIAN_NASAL_LINES_CROP, x_crop = True)
        r_raw_score = self._get_raw_score(nasal_junction_r, r_adjusted_lines)
        l_raw_score = self._get_raw_score(nasal_junction_l, l_adjusted_lines)
        r_score = self._score_threshold(r_raw_score, NASAL_LINES_THRESHOLD)
        l_score = self._score_threshold(l_raw_score, NASAL_LINES_THRESHOLD)
        overall_score = self._score_threshold(np.mean([r_raw_score, l_raw_score]), NASAL_LINES_THRESHOLD)
        return ((r_highlighted_image, r_score), (l_highlighted_image, l_score), overall_score)
    
    def get_overall_score(self, round_score = False):
        _, fh_score = self.get_forehead()        
        _, _, cf_score = self.get_crows_feet()
        _, _, be_score = self.get_below_eyes()
        _, _, nl_score = self.get_nasal_lines()
        score = FH_WEIGHT * fh_score + CF_WEIGHT * cf_score + BE_WEIGHT * be_score + NL_WEIGHT * nl_score
        if round_score:
            return int(round(score))
        return score

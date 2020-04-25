import cv2
import pickle
import numpy as np
from skin_tone_estimator import get_skin_tone_RGB
from sklearn.linear_model import LinearRegression
import imutils
import config

D_E_WIDTH_RESCALE = config.D_E_WIDTH_RESCALE
H_SPLIT_COEFF = config.H_SPLIT_COEFF
W_SPLIT_COEFF = config.W_SPLIT_COEFF
N_TOP_SELECT = config.N_TOP_SELECT


def split(x, n): 
    split = []
    if (x % n == 0): 
        last = 0
        for i in range(n): 
            last += x//n
            split.append(last)
    else: 
        zp = n - (x % n) 
        pp = x//n
        last = 0
        for i in range(n): 
            if(i>= zp):
                last += pp + 1
                split.append(last)
            else:
                last += pp
                split.append(last) 
    return split


class DarkEyeDetector():
    def __init__(self, facial_landmark, model):
        self.facial_landmark = facial_landmark
        self.image = facial_landmark.image
        self.score_model = model
    
    #[[RGB_sum, r, g, b]]
    def _custom_data_structure(self, img, y1, y2, x1, x2):
        dat = []
        crop = img[y1:y2, x1:x2]
        RGB = get_skin_tone_RGB(crop)
        totalRGB = np.sum(RGB)
        dat.append(totalRGB)
        for color in RGB:
            dat.append(color)
        return dat
    
    def _calculate_adjusted_dark_tone(self, img):
        h = img.shape[0]
        w = img.shape[1]
        h_split = split(h, H_SPLIT_COEFF)
        w_split = split(w, W_SPLIT_COEFF)
        pix_ar = []
        for i, _ in enumerate(h_split):
            for j, _ in enumerate(w_split):
                if i == 0:
                    y1 = 0
                else:
                    y1 = h_split[i-1]
                if j==0:
                    x1 = 0
                else:
                    x1 = w_split[j-1]
                y2 = h_split[i]
                x2 = w_split[j]
                pix_ar.append(self._custom_data_structure(img,y1,y2,x1,x2))
        pix_ar.sort()
        selected_patch = np.asarray(pix_ar[:N_TOP_SELECT])
        return (int(round(np.mean(selected_patch[:,1]))), int(round(np.mean(selected_patch[:,2]))), int(round(np.mean(selected_patch[:,3]))))

    def get_skin_tone(self):
        #utilizes forehead region for getting overall face color
        forehead_region = self.facial_landmark.get_forehead_region()
        forehead_region = imutils.resize(forehead_region, width = D_E_WIDTH_RESCALE)
        skin_tone = get_skin_tone_RGB(forehead_region)
        return skin_tone
    
    #return right and left tone in RGB
    def get_dark_eyes(self, darkest_only = False):
        below_eyes_r, below_eyes_l = self.facial_landmark.get_below_eyes_region()
        r_tone = self._calculate_adjusted_dark_tone(below_eyes_r)
        l_tone = self._calculate_adjusted_dark_tone(below_eyes_l)
        if darkest_only:
            r_sum = np.sum(r_tone)
            l_sum = np.sum(l_tone)
            if r_sum < l_sum:
                return r_tone
            else:
                return l_tone
        return (r_tone, l_tone)
    
    def get_score(self):
        face_tone = self.get_skin_tone()
        eye_tone = self.get_dark_eyes(darkest_only = True)
        dat = []
        for color in face_tone:
            dat.append(color)
        for color in eye_tone:
            dat.append(color)
        for i in range(3):
            diff = (face_tone[i] - eye_tone[i]) * 100 / face_tone[i]
            dat.append(diff)
        x = np.asarray([dat])
        pred = self.score_model.predict(x)
        pred[pred<0] = 0
        score = pred[0]
        return score
        
    
    
import cv2
import numpy as np

HSV_MAX = 170
YCRCB_MIN_1 = 130 
YCRCB_MAX_1 = 170
YCRCB_MIN_2 = 90
YCRCB_MAX_2 = 130


def _segment_otsu(image_grayscale, img_BGR):
    threshold_value, threshold_image = cv2.threshold(image_grayscale, 0, 255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    threshold_image_binary = 1- threshold_image/255
    threshold_image_binary = np.repeat(threshold_image_binary[:, :, np.newaxis], 3, axis=2)
    img_skin_only = np.multiply(threshold_image_binary, img_BGR)
    img_skin_only = np.array(img_skin_only, dtype=np.uint8)
    return img_skin_only

def get_skin_tone_RGB(img):
    img_grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_skin_only = _segment_otsu(img_grayscale, img)
    img_HSV = cv2.cvtColor(img_skin_only, cv2.COLOR_BGR2HSV)
    img_YCrCb = cv2.cvtColor(img_skin_only, cv2.COLOR_BGR2YCrCb)
    blue = []
    green = []
    red = []
    height, width, channels = img_skin_only.shape
    for i in range (height):
        for j in range (width):
            if((img_HSV.item(i, j, 0) <= HSV_MAX) and (YCRCB_MIN_1 <= img_YCrCb.item(i, j, 1) <= YCRCB_MAX_1) and (YCRCB_MIN_2 <= img_YCrCb.item(i, j, 2) <= YCRCB_MAX_2)):
                blue.append(img_skin_only[i, j].item(0))
                green.append(img_skin_only[i, j].item(1))
                red.append(img_skin_only[i, j].item(2))
    skin_tone_estimate_BGR = [np.mean(blue), np.mean(green), np.mean(red)]
    return (int(round(skin_tone_estimate_BGR[2])), int(round(skin_tone_estimate_BGR[1])), int(round(skin_tone_estimate_BGR[0])))
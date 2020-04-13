from acne_detection import AcneDetector
from age_gender_estimation import AgeGenderEstimator
from dark_eye_detection import DarkEyeDetector
from facial_landmark import FacialLandmark
from wrinkles_detection import WrinklesDetector
import cv2
import matplotlib.pyplot as plt
import json


def showImage(title, image):
    cv2.imshow(title, image)
    cv2.moveWindow(title,0,0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def printImage(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.show()


def plot_color(r, g, b):
    plt.imshow([[(r/255, g/255, b/255)]])
    plt.show()


def lambda_handler(event, context):
    file_path = "./test_images/image11.jpg"
    ori_img = cv2.imread(file_path)
    fl = FacialLandmark(ori_img)
    # printImage(fl.get_forehead_region())
    # printImage(fl.get_chin_region())
    r_cr, l_cr = fl.get_crows_feet_region()
    # printImage(r_cr)
    # printImage(l_cr)
    r_cr, l_cr = fl.get_below_eyes_region()
    # printImage(r_cr)
    # printImage(l_cr)
    r_cr, l_cr = fl.get_nasal_junction_region()
    # printImage(r_cr)
    # printImage(l_cr)
    r_cr, l_cr = fl.get_cheeks_region()
    # printImage(r_cr)
    # printImage(l_cr)
    ag = AgeGenderEstimator(fl)
    print("Age gender:", ag.predict_age_gender())

    de = DarkEyeDetector(fl)
    # plot_color(*de.get_skin_tone())
    # print("skin tone")
    r, l = de.get_dark_eyes()
    # plot_color(*r)
    # print("right dark eye")
    # plot_color(*l)1
    # print("left dark eye")
    print("Dark eye score: ", de.get_score())

    ad = AcneDetector(fl)
    print("Acne score:", ad.get_overall_score())
    wd = WrinklesDetector(fl)
    print("Wrinkle score:", wd.get_overall_score())

    if event['httpMethod'] == 'POST':
        body = event['body']
        return {
            'statusCode': 200,
            'body': json.dumps({
                'imgstring': body
            })
        }

    else:
        return {
            'statusCode': 200,
            'body': json.dumps('Please use POST request!')
        }

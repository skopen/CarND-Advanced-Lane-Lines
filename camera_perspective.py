
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle
import time
import datetime

debug = False

PERSPECTIVE_TRANSFORM = None
INVERSE_PERSPECTIVE_TRANSFORM = None
XM_PER_PIX = 3.7 / (1011 - 200)
YM_PER_PIX = 3 / (215 - 140)

def configureTransformMatrix(forceRecompute):
    global PERSPECTIVE_TRANSFORM, INVERSE_PERSPECTIVE_TRANSFORM

    if (forceRecompute == False):
        try:
            dist_pickle = pickle.load(open("./my_cached_data/transform_data.p", "rb"))
            TIME = dist_pickle["TIME"]
            PERSPECTIVE_TRANSFORM = dist_pickle["PERSPECTIVE_TRANSFORM"]
            INVERSE_PERSPECTIVE_TRANSFORM = dist_pickle["INVERSE_PERSPECTIVE_TRANSFORM"]
            if debug: print("Loaded prior transform data from " + TIME + ". Send forceRecompute=True for recomputation.")
            return
        except:
            print("Could not load from prior transform data. Recomputing transform...")
            pass

    src = np.float32([[180, 720], [582, 455], [700, 455], [1130, 720]])
    dst = np.float32([[180, 720], [160, 0], [1150, 0], [1130, 720]])

    PERSPECTIVE_TRANSFORM = cv2.getPerspectiveTransform(src, dst)
    INVERSE_PERSPECTIVE_TRANSFORM = cv2.getPerspectiveTransform(dst, src)
    print ("Saving transform data for future calculations...")
    dist_pickle = {"TIME":datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), "PERSPECTIVE_TRANSFORM":PERSPECTIVE_TRANSFORM, "INVERSE_PERSPECTIVE_TRANSFORM": INVERSE_PERSPECTIVE_TRANSFORM}
    pickle.dump(dist_pickle, open("./my_cached_data/transform_data.p", "wb"))

    if debug:
        img = mpimg.imread("./test_images/straight_lines1.jpg")
        cv2.line(img, (src[0][0], src[0][1]), (src[1][0], src[1][1]), [255, 0, 0], 2)
        cv2.line(img, (src[1][0], src[1][1]), (src[2][0], src[2][1]), [255, 0, 0], 2)
        cv2.line(img, (src[2][0], src[2][1]), (src[3][0], src[3][1]), [255, 0, 0], 2)
        cv2.line(img, (src[3][0], src[3][1]), (src[0][0], src[0][1]), [255, 0, 0], 2)
        cv2.imwrite("./output_images/output_straight_lines1_pre_perspective.jpg", img)

        img = mpimg.imread("./test_images/straight_lines1.jpg")
        txImg = transform(img)

        cv2.line(txImg, (dst[0][0], dst[0][1]), (dst[0][0], 0), [255, 0, 0], 2)
        cv2.line(txImg, (dst[3][0], dst[3][1]), (dst[3][0], 0), [255, 0, 0], 2)

        cv2.imwrite("./output_images/output_straight_lines1_post_perspective.jpg", txImg)

        plt.imshow(img)
        plt.show()

        plt.imshow(txImg)
        plt.show()

def transform(img):
    imgSize = (img.shape[1], img.shape[0])
    tx = cv2.warpPerspective(img, PERSPECTIVE_TRANSFORM, imgSize, flags=cv2.INTER_LINEAR)
    return tx

def inverseTransform(img):
    imgSize = (img.shape[1], img.shape[0])
    invTx = cv2.warpPerspective(img, INVERSE_PERSPECTIVE_TRANSFORM, imgSize, flags=cv2.INTER_LINEAR)
    return invTx

def covertPixToMeters(x, y):
    return XM_PER_PIX*x, YM_PER_PIX*y

def pixX2M(x):
    return XM_PER_PIX*x

def pixY2M(y):
    return YM_PER_PIX*y
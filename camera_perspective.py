
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import pickle
import time
import datetime

debug = True

PERSPECTIVE_TRANSFORM = None
INVERSE_PERSPECTIVE_TRANSFORM = None

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

    src_top_leftx = 582
    src_bottom_leftx = 240

    src = np.float32(
        [[src_bottom_leftx, 665], [src_top_leftx, 455], [1280 - src_top_leftx, 455], [1280 - src_bottom_leftx, 665]])
    dst = np.float32([[240, 720], [240, 0], [1040, 0], [1040, 720]])

    PERSPECTIVE_TRANSFORM = cv2.getPerspectiveTransform(src, dst)
    INVERSE_PERSPECTIVE_TRANSFORM = cv2.getPerspectiveTransform(dst, src)
    print ("Saving transform data for future calculations...")
    dist_pickle = {"TIME":datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), "PERSPECTIVE_TRANSFORM":PERSPECTIVE_TRANSFORM, "INVERSE_PERSPECTIVE_TRANSFORM": INVERSE_PERSPECTIVE_TRANSFORM}
    pickle.dump(dist_pickle, open("./my_cached_data/transform_data.p", "wb"))

    if debug:
        img = mpimg.imread("./test_images/straight_lines1.jpg")
        txImg = transform(img)
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
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import pickle
import time
import datetime

debug = False

DISTORTION_COEFF = None
CAMERA_MATRIX = None

def calibrateCamera (calibrationImgLocation, chessBoardSizeX, chessBoardSizeY, forceRecalibrate):
    global CAMERA_MATRIX, DISTORTION_COEFF

    if (forceRecalibrate == False):
        try:
            dist_pickle = pickle.load(open("./my_cached_data/calibration_data.p", "rb"))
            TIME = dist_pickle["TIME"]
            CAMERA_MATRIX = dist_pickle["CAMERA_MATRIX"]
            DISTORTION_COEFF = dist_pickle["DISTORTION_COEFF"]
            if debug: print("Loaded prior calibration data from " + TIME + ". Send forceRecalibrate=True for recomputation.")
            return
        except:
            print("Could not load from prior calibration data. Recomputing calibration...")
            pass

    calibrationImages = glob.glob(calibrationImgLocation + "/calibration*.jpg")
    objPoints = [] # 3D points in real world space
    imgPoints = [] # 2D points in image space
    objp = np.zeros((chessBoardSizeX*chessBoardSizeY, 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessBoardSizeX, 0:chessBoardSizeY].T.reshape(-1, 2) # x, y, coordinates

    for fname in calibrationImages:
        print("Processing calibration image: " + fname)

        # read the image
        img = mpimg.imread(fname)

        # convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # find chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, (chessBoardSizeX, chessBoardSizeY), None)

        if ret == True:
            imgPoints.append(corners)
            objPoints.append(objp)

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, gray.shape[::-1], None, None)
        CAMERA_MATRIX = mtx
        DISTORTION_COEFF = dist

    print ("Saving distortion coefficients and matrix for future calculations...")
    dist_pickle = {"TIME":datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), "CAMERA_MATRIX":CAMERA_MATRIX, "DISTORTION_COEFF": DISTORTION_COEFF}
    pickle.dump(dist_pickle, open("./my_cached_data/calibration_data.p", "wb"))


# Performs image distortion correction based on the computed distortion coefficients and camera matrix
# returns the undistorted image
def undistortImage (img):
    if debug: print("Undistorting with... " + str(DISTORTION_COEFF))

    undist = cv2.undistort(img, CAMERA_MATRIX, DISTORTION_COEFF, None, CAMERA_MATRIX)

    if debug:
        plt.imshow(undist)
        plt.show()

    return undist

def printInfo():
    print (CAMERA_MATRIX)
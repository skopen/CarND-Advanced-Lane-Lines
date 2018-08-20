from camera_calibrate import *
from camera_perspective import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

calibrateCamera ("./camera_cal", 9, 6, False)

img = mpimg.imread("./camera_cal/calibration16.jpg")

undistortImage(img)

configureTransformMatrix(True)


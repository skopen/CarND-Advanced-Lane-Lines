from camera_calibrate import *

calibrateCamera ("./camera_cal", 9, 6, False)

img = mpimg.imread("./camera_cal/calibration16.jpg")

undistortImage(img)

#[[-0.23185373 -0.11832121 -0.00116562  0.00023901  0.15356231]]
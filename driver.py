from camera_calibrate import *
from camera_perspective import *
from thresholded_binary import *
from polyfit_init import *
from polyfit_next import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from moviepy.editor import VideoFileClip
from main_image_processor import *
from camera_calibrate import *
from thresholded_binary import *
from camera_perspective import *
from polyfit_init import *

def processVideos():
    initProcessor(False)
    process_video("project_video.mp4")
    #process_video("challenge_video.mp4")
    #process_video("harder_challenge_video.mp4")

def processImages():
    initProcessor(False)
    imagesNames = ["straight_lines1.jpg", "straight_lines2.jpg", "test1.jpg", "test2.jpg", "test3.jpg", "test4.jpg", "test5.jpg", "test6.jpg"]
    for fname in imagesNames:
        print("Processing image: " + fname)
        # read the image
        img = mpimg.imread("test_images/" + fname)
        imgWithLaneMarked = process_image(img)
        cv2.imwrite("output_images/output_"+fname, imgWithLaneMarked)

def createSampleUndistortedImage():
    initProcessor(False)
    img = mpimg.imread("camera_cal/calibration1.jpg")
    undist = undistortImage(img)
    cv2.imwrite("output_images/output_calibration1.jpg", undist)

    img = mpimg.imread("test_images/straight_lines1.jpg")
    undist = undistortImage(img)
    cv2.imwrite("output_images/output_straight_lines1_undistorted.jpg", undist)

def createSampleThresholdedBinaryImage():
    img = mpimg.imread("test_images/straight_lines1.jpg")
    binImg = createThresholdedBinary(img)
    color_binary = np.dstack((binImg, binImg, binImg)) * 255
    cv2.imwrite("output_images/output_straight_lines1_threshold_binary.jpg", color_binary)

def createSampleTramsformedImage():
    initProcessor(False)
    img = mpimg.imread("test_images/straight_lines1.jpg")
    imgUndist = undistortImage(img)
    img = createThresholdedBinary(imgUndist)
    imgTrans = transform(img)
    color_binary = np.dstack((imgTrans, imgTrans, imgTrans)) * 255
    cv2.imwrite("output_images/output_straight_lines1_transformed.jpg", color_binary)

def plotFittedLane():
    initProcessor(False)

    img = mpimg.imread("test_images/test2.jpg")
    imgUndist = undistortImage(img)
    img = createThresholdedBinary(imgUndist)
    imgTrans = transform(img)
    #color_binary = np.dstack((imgTrans, imgTrans, imgTrans)) * 255
    #left_fit, right_fit = fit_polynomial(imgTrans)

    left_fit, right_fit, result = fit_polynomial(imgTrans)

    #result, left_fit, right_fit, overall_confidence = search_around_poly(imgTrans, imgUndist, left_fit, right_fit, False)



    cv2.imwrite("output_images/output_test2_fitted.jpg", result)

#processImages()
#createSampleUndistortedImage()
#createSampleThresholdedBinaryImage()
#createSampleTramsformedImage()
plotFittedLane()
from camera_calibrate import *
from camera_perspective import *
from thresholded_binary import *
from polyfit_init import *
from polyfit_next import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from moviepy.editor import VideoFileClip

def init (forceFullInit):
    calibrateCamera ("./camera_cal", 9, 6, forceFullInit)
    configureTransformMatrix(forceFullInit)

def process_image(imgOrig):
    img = np.copy(imgOrig)
    imgUndist = undistortImage(img)
    img = createThresholdedBinary(imgUndist)
    imgTrans = transform(img)
    leftx, lefty, rightx, righty, out_img = find_lane_pixels(imgTrans)
    left_fitx, right_fitx, ploty, left_fit, right_fit = fit_poly(imgTrans.shape, leftx, lefty, rightx, righty)
    imgWithLaneMarked = search_around_poly(imgTrans, imgUndist, left_fit, right_fit)
    return imgWithLaneMarked

def process_video(inputFile):
    outputFullFile = "output_images/output_" + inputFile
    clip1 = VideoFileClip(inputFile).subclip(0, 5)
    white_clip = clip1.fl_image(process_image)
    white_clip.write_videofile(outputFullFile, audio=False)

init(False)
process_video("project_video.mp4")
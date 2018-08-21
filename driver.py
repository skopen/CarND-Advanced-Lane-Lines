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

start = True
curr_left_fit = None
curr_right_fit = None
lowConfidenceRetries = 0

def process_image(imgOrig):

    global start, curr_left_fit, curr_right_fit, lowConfidenceRetries

    img = np.copy(imgOrig)
    imgUndist = undistortImage(img)
    img = createThresholdedBinary(imgUndist)
    imgTrans = transform(img)
    imgWithLaneMarked = None


    while(True):
        if (start):
            start = False
            leftx, lefty, rightx, righty, out_img = find_lane_pixels(imgTrans)
            left_fitx, right_fitx, ploty, curr_left_fit, curr_right_fit = fit_poly(imgTrans.shape, leftx, lefty, rightx, righty, False, None, None)
            imgWithLaneMarked, curr_left_fit, curr_right_fit, overall_confidence = search_around_poly(imgTrans, imgUndist, curr_left_fit, curr_right_fit, False)
            break

        imgWithLaneMarked, curr_left_fit, curr_right_fit, overall_confidence = search_around_poly(imgTrans, imgUndist, curr_left_fit, curr_right_fit, False)

        if (overall_confidence < 0.7):
            lowConfidenceRetries += 1
            if (lowConfidenceRetries < 4):
                #print("\nUsing older fit due to low confidence...")
                imgWithLaneMarked, curr_left_fit, curr_right_fit, overall_confidence = search_around_poly(imgTrans, imgUndist, curr_left_fit, curr_right_fit, True)
                break
            else:
                #print("\nReprocessing from start, did not find a good frame...")
                start = True
                lowConfidenceRetries = 0
        else:
            lowConfidenceRetries = 0
            break

    return imgWithLaneMarked

def process_video(inputFile):
    start = True
    outputFullFile = "output_images/output_" + inputFile
    #clip1 = VideoFileClip(inputFile).subclip(0, 5)
    clip1 = VideoFileClip(inputFile)
    white_clip = clip1.fl_image(process_image)
    white_clip.write_videofile(outputFullFile, audio=False)

init(False)
#process_video("project_video.mp4")
#process_video("challenge_video.mp4")
process_video("harder_challenge_video.mp4")

from camera_calibrate import *
from camera_perspective import *
from thresholded_binary import *
from polyfit_init import *
from polyfit_next import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from moviepy.editor import VideoFileClip


calibrateCamera ("./camera_cal", 9, 6, False)
configureTransformMatrix(False)

imgOrig = mpimg.imread("./test_images/straight_lines2.jpg")

def process_image(imgOrig):
    img = np.copy(imgOrig)

    imgUndist = undistortImage(img)

    img = createThresholdedBinary(imgUndist)

    imgTrans = transform(img)

    leftx, lefty, rightx, righty, out_img = find_lane_pixels(imgTrans)
    left_fitx, right_fitx, ploty, left_fit, right_fit = fit_poly(imgTrans.shape, leftx, lefty, rightx, righty)

    imgWithLaneMarked = search_around_poly(imgTrans, imgUndist, left_fit, right_fit)

    return imgWithLaneMarked


inputFile = "harder_challenge_video.mp4"
outputFullFile = "output_images/output_" + inputFile

## To speed up the testing process you may want to try your pipeline on a shorter subclip of the video
## To do so add .subclip(start_second,end_second) to the end of the line below
## Where start_second and end_second are integer values representing the start and end of the subclip
## You may also uncomment the following line for a subclip of the first 5 seconds
##clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4").subclip(0,5)
clip1 = VideoFileClip(inputFile).subclip(0, 5)
white_clip = clip1.fl_image(process_image)
white_clip.write_videofile(outputFullFile, audio=False)


#plt.show()

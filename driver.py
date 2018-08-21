from camera_calibrate import *
from camera_perspective import *
from thresholded_binary import *
from polyfit_init import *
from polyfit_next import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


calibrateCamera ("./camera_cal", 9, 6, False)
configureTransformMatrix(False)

imgOrig = mpimg.imread("./test_images/straight_lines2.jpg")

img = np.copy(imgOrig)

imgUndist = undistortImage(img)

img = createThresholdedBinary(imgUndist)

imgTrans = transform(img)


leftx, lefty, rightx, righty, out_img = find_lane_pixels(imgTrans)
left_fitx, right_fitx, ploty, left_fit, right_fit = fit_poly(imgTrans.shape, leftx, lefty, rightx, righty)

imgWithLaneMarked = search_around_poly(imgTrans, imgUndist, left_fit, right_fit)

plt.imshow(imgWithLaneMarked)

# Plot the result
# f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
# f.tight_layout()
#
# ax1.imshow(imgTrans)
# ax1.set_title('Original Image', fontsize=40)
#
# ax2.imshow(out_img)
# ax2.set_title('Pipeline Result', fontsize=40)
# plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)

plt.show()

from camera_calibrate import *
from camera_perspective import *
from thresholded_binary import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

calibrateCamera ("./camera_cal", 9, 6, False)
configureTransformMatrix(False)

img = mpimg.imread("./test_images/straight_lines1.jpg")

img = undistortImage(img)

img = createThresholdedBinary(img)

imgTrans = transform(img)




# Plot the result
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
f.tight_layout()

ax1.imshow(img)
ax1.set_title('Original Image', fontsize=40)

ax2.imshow(imgTrans)
ax2.set_title('Pipeline Result', fontsize=40)
plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)

plt.show()

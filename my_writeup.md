## Advanced Lane Finding Project Writeup

### 

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./examples/undistort_output.png "Undistorted"
[image2]: ./test_images/test1.jpg "Road Transformed"
[image3]: ./examples/binary_combo_example.jpg "Binary Example"
[image4]: ./examples/warped_straight_lines.jpg "Warp Example"
[image5]: ./examples/color_fit_lines.jpg "Fit Visual"
[image6]: ./examples/example_output.jpg "Output"
[image7]: ./output_images/output_calibration1.jpg "Output Calibration"
[image8]: ./output_images/output_straight_lines1.jpg "Output straight lines"
[image9]: ./output_images/output_straight_lines1_fitted.jpg "Output fitted"
[image10]: ./output_images/output_straight_lines1_threshold_binary.jpg "Threshold binary"
[image11]: ./output_images/output_straight_lines1_transformed.jpg "Transformed"
[image12]: ./output_images/output_straight_lines1_undistorted.jpg "Undistorted"
[image13]: ./output_images/output_straight_lines2.jpg "Straight lines 2"
[image14]: ./output_images/output_test1.jpg "Test 1"
[image15]: ./output_images/output_test2_fitted.jpg "Test 2 Fitted"
[image16]: ./camera_cal/calibration1.jpg "Calibration image original"
[image17]: ./test_images/straight_lines1.jpg "Straight lines 1 original image"
[image18]: ./output_images/output_straight_lines1_pre_perspective.jpg "Pre-perspective"
[image19]: ./output_images/output_straight_lines1_post_perspective.jpg "Post-perspective"
[video1]: ./project_video.mp4 "Project Video"
[video2]: ./output_images/output_project_video.mp4 "Project Video Output"


## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here is my description of the project and how I addressed the key requirements of the rubric.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

Below you will find the writeup for the project.

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is located in [camera_calibrate.py](./camera_calibrate.py).  

I first created the object points, which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result by calling `createSampleUndistortedImage()` function in [driver.py](./driver.py): 

Original Image:
![alt text][image16]

Calibrated Image:
![alt text][image7]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

Further, I applied distortion correction to this image:

![alt text][image17]

And obtained the following undistorted image:

![alt text][image12]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image. The corresponding code is in function createThresholdedBinary() in [thresholded_binary.py](./thresholded_binary.py). 
Here's an example of my output for this step:

![alt text][image10]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform is in [camera_perspective.py](./camera_perspective.py).
The `configureTransformMatrix` function creates the transformation matrix and saves it, while the `transform()` method applies the 
transform to the passed in image. I chose to hardcode the source and destination points in the following manner:

```python
    src = np.float32([[180, 720], [582, 455], [700, 455], [1130, 720]])
    dst = np.float32([[180, 720], [160, 0], [1150, 0], [1130, 720]])
```

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

Before transform, the image looks like:
![alt text][image18]

After the transform the image look like:
![alt text][image19]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Then I implemented the lane-line pixel identification code. I performed a histogram of the bottom half of the transformed image to identify most
likely location of the two lanes. After the location was identified, I performed a window search by moving up the lane within a specific margin\
looking for potential lane-line pixels. This code is implemented in [polyfit_init.py](./polyfit_init.py).

Two examples of such lane-line pixels identification and then fitting with a second order polynomial are:

Example 1:
![alt text][image9]

Example 2:
![alt text][image15]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.
 
I identified the lane curvature by applying the lane curvature formula given the function (in our case the second order polynomial function). 
Since the location of the camera is given to be in the center of the vehicle, we can use this information to find the center offset. I calculated
the offset by subtracting the average of the lanes x-coordinates from the vehicle center location. Both of these calculations are done in the
`getFrameStats()` function defined in [polyfit_next.py](./polyfit_next.py).

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

Here are a couple of examples of my result:

Example 1:
![alt text][image8]

Example 2:
![alt text][image14]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./output_images/output_project_video.mp4)

---

### Discussion

Here are the main issues I encountered and some areas of improvement:

1. The toughest part was identification of the lanes. I believe the current algorithm we have used is fairly restrictive.
I can think of a better and more intuitive algorithm, which I would like to implement.
2. I am not sure if 2-degree polynomial is the right fit for some road conditions (espcially when field of view is long
and the road is curvy). I would like to try 3rd degree; we need to see it does not overfit in certain cases.
3. My algorithm has a harder time when the road has other high gradient features on the the lane. I think this part
should be augmented with additional algorithms or smoothing methods.
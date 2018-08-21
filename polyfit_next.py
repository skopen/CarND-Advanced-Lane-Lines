from camera_perspective import *
import math


def fit_poly(img_shape, leftx, lefty, rightx, righty, reuseOldFit, left_fit, right_fit):

    if (reuseOldFit == False):
        ### Fit a second order polynomial to each with np.polyfit() ###
        left_fit = np.polyfit(lefty, leftx, 2)
        right_fit = np.polyfit(righty, rightx, 2)

    # Generate x and y values for plotting
    ploty = np.linspace(0, img_shape[0] - 1, img_shape[0])
    ### Calc both polynomials using ploty, left_fit and right_fit ###
    left_fitx = left_fit[0] * ploty ** 2 + left_fit[1] * ploty + left_fit[2]
    right_fitx = right_fit[0] * ploty ** 2 + right_fit[1] * ploty + right_fit[2]

    return left_fitx, right_fitx, ploty, left_fit, right_fit


def search_around_poly(binary_warped, imgOrigUndist, left_fit, right_fit, reuseOldFit):
    # HYPERPARAMETER
    margin = 100

    # Grab activated pixels
    nonzero = binary_warped.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])

    ### Set the area of search based on activated x-values ###
    ### within the +/- margin of our polynomial function ###
    left_lane_inds = ((nonzerox > (left_fit[0] * (nonzeroy ** 2) + left_fit[1] * nonzeroy +
                                   left_fit[2] - margin)) & (nonzerox < (left_fit[0] * (nonzeroy ** 2) +
                                                                         left_fit[1] * nonzeroy + left_fit[
                                                                             2] + margin))).nonzero()[0]
    right_lane_inds = ((nonzerox > (right_fit[0] * (nonzeroy ** 2) + right_fit[1] * nonzeroy +
                                    right_fit[2] - margin)) & (nonzerox < (right_fit[0] * (nonzeroy ** 2) +
                                                                           right_fit[1] * nonzeroy + right_fit[
                                                                               2] + margin))).nonzero()[0]

    # Again, extract left and right line pixel positions
    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds]
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]

    # Fit new polynomials
    left_fitx, right_fitx, ploty, left_fit, right_fit = fit_poly(binary_warped.shape, leftx, lefty, rightx, righty, reuseOldFit, left_fit, right_fit)

    # Create an image to draw the lines on
    warp_zero = np.zeros_like(binary_warped).astype(np.uint8)
    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

    # Recast the x and y points into usable format for cv2.fillPoly()
    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    pts = np.hstack((pts_left, pts_right))

    # Draw the lane onto the warped blank image
    cv2.fillPoly(color_warp, np.int_([pts]), (0, 255, 0))

    # Warp the blank back to original image space using inverse perspective matrix (Minv)
    newwarp = inverseTransform(color_warp)
    #newwarp = color_warp

    # Combine the result with the original image
    result = cv2.addWeighted(imgOrigUndist, 1, newwarp, 0.3, 0)

    left_curv, right_curv, offset, laneConf, curvConf, slopeConf = getFrameStats(left_fitx, right_fitx, ploty)
    overall_confidence = laneConf*curvConf*slopeConf

    # add curvature nad center offset info
    cv2.putText(result, "Rad of Curvature:  Left: " + str(int(left_curv)) + "m", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.putText(result, "Rad of Curvature: Right: " + str(int(right_curv)) + "m", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.putText(result, "Center offset: " + str(round(offset, 2)) + "m", (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.putText(result, "Lane Width Confidence: " + str(round(laneConf, 3)), (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.putText(result, "Curvature Confidence: " + str(round(curvConf, 3)), (20, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.putText(result, "Slope Confidence: " + str(round(slopeConf, 3)), (20, 280), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.putText(result, "Overall Confidence: " + str(round(overall_confidence, 3)), (20, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    return result, left_fit, right_fit, overall_confidence


def getFrameStats (left_fitx, right_fitx, ploty):
    # Define y-value where we want radius of curvature
    # We'll choose the maximum y-value, corresponding to the bottom of the image
    y_eval = pixY2M(np.max(ploty))

    left_fit_cr = np.polyfit(pixY2M(ploty), pixX2M(left_fitx), 2)
    right_fit_cr = np.polyfit(pixY2M(ploty), pixX2M(right_fitx), 2)

    #Implement the calculation of R_curve (radius of curvature) #####
    left_curverad = ((1 + (2 * left_fit_cr[0] * y_eval + left_fit_cr[1]) ** 2) ** 1.5) / np.absolute(2 * left_fit_cr[0])
    right_curverad = ((1 + (2 * right_fit_cr[0] * y_eval + right_fit_cr[1]) ** 2) ** 1.5) / np.absolute(2 * right_fit_cr[0])

    leftX = left_fit_cr[0]*y_eval**2 + left_fit_cr[1]*y_eval + left_fit_cr[2]
    rightX = right_fit_cr[0]*y_eval**2 + right_fit_cr[1]*y_eval + right_fit_cr[2]
    lane_center = (leftX + rightX)/2.0;
    car_center = pixX2M(1280/2.0)
    offset = lane_center - car_center

    confidence = 1.0

    actualLaneWidth = rightX - leftX

    # lane confidence = 1/e^((actual_lane_width - expected_lane_width)**2)
    laneWidthNormalDiff = ((actualLaneWidth - 3.7) / 3.7) ** 2

    if (laneWidthNormalDiff > 10):
        laneWidthConfidence = 0.0
    else:
        laneWidthConfidence = 1.0 / (math.e**laneWidthNormalDiff)


    meanCurv = (left_curverad + right_curverad)/2
    curvNormalDiff = ((right_curverad - left_curverad)/meanCurv)**2

    if (curvNormalDiff > 10):
        curvatureConfidence = 0.0
    else:
        curvatureConfidence = 1.0 / (math.e**curvNormalDiff)

    # since most of slopes (note it is dx/dy) we get will be close to 0, we need to apply some additional computation
    # we will do tan-inverse to get the slope angle, which will also be close to 0, and then add 0.1 to rotate by atan(0.1)
    # Then do the difference between the computed angles which should be equivalent to comparing with original slopes.
    slopeLeft = math.atan(2*left_fit_cr[0]*y_eval + left_fit_cr[1]) + 0.1
    slopeRight = math.atan(2*right_fit_cr[0]*y_eval + right_fit_cr[1]) + 0.1
    meanSlope = (slopeLeft + slopeRight) / 2
    slopeNormalDiff = ((slopeRight - slopeLeft)/meanSlope)**2

    if (slopeNormalDiff > 10):
        slopeConfidence = 0.0
    else:
        slopeConfidence = 1.0 / (math.e**slopeNormalDiff)

    return left_curverad, right_curverad, offset, laneWidthConfidence, curvatureConfidence, slopeConfidence



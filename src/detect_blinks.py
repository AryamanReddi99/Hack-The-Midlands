# detect_blinks.py

# This file is created from source code and examples taken from
# https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/
#
# This demo uses the pre-trained shape predictor values found here:
# http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
# This site explains how to train your own shape predictor:
# http://dlib.net/face_landmark_detection.py.html

# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
from matplotlib import pyplot as plt
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import collections

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear


# Graphing
ears = []
eyeopens = []
filtered = []
filtered_der = []
filtered_superlo = []
ear_filtered_superlo = 0.2
means = []
stdevs = []
sumn = 0.0
sumnsq = 0.0
ctrs = []
ctr = 0

window = collections.deque()

mean_maxs = []

ar_ests = []
ar_est = 0.0

thresh_high = []
thresh_low = []

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
                help="path to facial landmark predictor")
ap.add_argument("-v", "--video", type=str, default="",
                help="path to input video file")
args = vars(ap.parse_args())

# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3

# Eye upper and lower threshold for eye open-close detection
EYE_AR_THRESH_UPPER = 0.2
EYE_AR_THRESH_LOWER = 0.15

# Eye AR derivative threshold for open/close detection
EYE_AR_DER_THRESH_UPPER = 0.015
EYE_AR_DER_THRESH_LOWER = -0.015


# initialize the frame counters and the total number of blinks
COUNTER = 0
TOTAL = 0

eyeopen = True

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video stream thread
print("[INFO] starting video stream thread...")
if (args["video"] == ""):
    vs = VideoStream(src=0).start()
    # vs = VideoStream(usePiCamera=True).start()
    fileStream = False
else:
    vs = FileVideoStream(args["video"]).start()
    fileStream = True
time.sleep(1.0)

# loop over frames from the video stream
while True:
    # if this is a file video stream, then we need to check if
    # there any more frames left in the buffer to process
    if fileStream and not vs.more():
        break

    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale
    # channels)
    frame = vs.read()
    if frame is None:
        break
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale frame
    rects = detector(gray, 0)

    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # average the eye aspect ratio together for both eyes
        ear = (leftEAR + rightEAR) / 2.0

        # compute the convex hull for the left and right eye, then
        # visualize each of the eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
        # add ear value to list
        if len(filtered) == 0:
            ear_filtered = ear
            ear_filtered_der = 0.0
        else:
            ear_filtered = 0.2 * ear + 0.8 * filtered[-1]
            if len(filtered_der) == 0:
                ear_filtered_der = ear_filtered - filtered[-1]
            else:
                ear_filtered_der = 0.2 * (ear_filtered - filtered[-1]) + 0.8 * filtered_der[-1]

        if len(filtered_superlo) == 0:
            ear_filtered_superlo = ear
        else:
            ear_filtered_superlo = 0.001 * ear + 0.999 * filtered_superlo[-1]

        sumn += ear
        sumnsq += ear*ear
        if ctr == 0:
            means.append(sumn)
            stdevs.append(0.0)
        else:
            means.append(sumn / ctr)
            stdevs.append(np.sqrt(sumnsq / ctr - (sumn / ctr)*(sumn / ctr)))

        filtered.append(ear_filtered)
        filtered_der.append(ear_filtered_der)
        filtered_superlo.append(ear_filtered_superlo)
        ears.append(ear)
        eyeopens.append(eyeopen)
        ctrs.append(ctr)
        ctr += 1
        mean_maxs.append(np.mean(np.array(sorted(list(window)[-150:]))))
        window.append(ear)
        if len(window) > 500:
            window.popleft()

        ar_est = ear
        ar_ests.append(ar_est)

        thresh_low.append(mean_maxs[-1] - 0.5 * stdevs[-1])
        thresh_high.append(mean_maxs[-1])
        

        if eyeopen and ar_est < thresh_low[-1]:
            eyeopen = False
        elif not eyeopen and ar_est > thresh_high[-1]:
            eyeopen = True
            TOTAL += 1
        # check to see if the eye aspect ratio is below the blink
        # threshold, and if so, increment the blink frame counter
        if ear < EYE_AR_THRESH:
            COUNTER += 1

        # otherwise, the eye aspect ratio is not below the blink
        # threshold
        else:
            # if the eyes were closed for a sufficient number of
            # then increment the total number of blinks
            #if COUNTER >= EYE_AR_CONSEC_FRAMES:
            #    TOTAL += 1

            # reset the eye frame counter
            COUNTER = 0

        # draw the total number of blinks on the frame along with
        # the computed eye aspect ratio for the frame
        cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()


plt.plot(ctrs, ears)
plt.plot(ctrs, eyeopens)
plt.plot(ctrs, filtered)
#plt.plot(ctrs, means)
#plt.plot(ctrs, stdevs)
plt.plot(ctrs, mean_maxs)
#plt.plot(ctrs, filtered_superlo)
#plt.plot(ctrs, filtered_der)
plt.plot(ctrs, ar_ests)
plt.plot(ctrs, thresh_high)
plt.plot(ctrs, thresh_low)
plt.show()


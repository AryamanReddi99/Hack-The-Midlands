# BlinkDetector.py

# This file is created from source code and examples taken from
# https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/
#
# This demo uses the pre-trained shape predictor values found here:
# http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
# This site explains how to train your own shape predictor:
# http://dlib.net/face_landmark_detection.py.html

from PyQt5 import QtCore
from scipy.spatial import distance as dist
from imutils import face_utils
from matplotlib import pyplot as plt
import numpy as np
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

class BlinkDetector(QtCore.QObject):
    lowerthresh = []
    upperthresh = []
    ar_est = []
    ctrs = []
    ctr = 0
    eyeopens = []

    result = QtCore.pyqtSignal(np.ndarray)

    # define two constants, one for the eye aspect ratio to indicate
    # blink and then a second constant for the number of consecutive
    # frames the eye must be below the threshold
    EYE_AR_THRESH = 0.3
    EYE_AR_CONSEC_FRAMES = 3

    # Eye upper and lower threshold for eye open-close detection
    EYE_AR_THRESH_UPPER = 0.2
    EYE_AR_THRESH_LOWER = 0.15

    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0

    # Eye open state
    eyeOpen = True

    # Values used in detection algorithm
    n = 0.0
    sumN = 0.0
    sumNSquared = 0.0
    sampleWindow = collections.deque()

    # Sample window size constants
    WINDOW_SIZE = 500
    WINDOW_SUBSET_SIZE = 200

    def __init__(self, file_shape_predictor):
        super(BlinkDetector, self).__init__()

        # initialize dlib's face detector (HOG-based) and then create
        # the facial landmark predictor
        print("[INFO] loading facial landmark predictor...")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(file_shape_predictor)

        # grab the indexes of the facial landmarks for the left and
        # right eye, respectively
        (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    @QtCore.pyqtSlot(np.ndarray)
    def handle_frame(self, frame):
        frame = imutils.resize(frame, width=1000)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = self.detector(gray, 0)

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[self.lStart:self.lEnd]
            rightEye = shape[self.rStart:self.rEnd]
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

            # Update totals
            self.n += 1.0
            self.sumN += ear
            self.sumNSquared += ear*ear

            # Update sliding window
            self.sampleWindow.append(ear)
            if len(self.sampleWindow) > self.WINDOW_SIZE:
                self.sampleWindow.popleft()

            # Calculate new std deviation
            stdDev = np.sqrt(self.sumNSquared / self.n - (self.sumN / self.n) ** 2)

            # Calculate mean of max subset
            maxMean = np.mean(np.sort(np.array(list(self.sampleWindow)))[-1*self.WINDOW_SUBSET_SIZE:])

            # Calculate the median(ish) - the point 2/3 through the sorted data
            medianish = sorted(list(self.sampleWindow))[(len(self.sampleWindow) * 2)//3]

            # Generate dynamic blink thresholds
            threshLower = medianish - 1.5 * stdDev
            threshUpper = medianish - 0.5 * stdDev

            self.upperthresh.append(threshUpper)
            self.lowerthresh.append(threshLower)
            self.ar_est.append(ear)
            self.ctrs.append(self.ctr)
            self.ctr+=1

            # Check if eye has changed state
            if self.eyeOpen and ear < threshLower:
                self.eyeOpen = False
            elif not self.eyeOpen and ear > threshUpper:
                self.eyeOpen = True
                self.TOTAL += 1

            self.eyeopens.append(self.eyeOpen)

            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            if ear < self.EYE_AR_THRESH:
                self.COUNTER += 1

            # otherwise, the eye aspect ratio is not below the blink
            # threshold
            else:
                # if the eyes were closed for a sufficient number of
                # then increment the total number of blinks
                #if self.COUNTER >= self.EYE_AR_CONSEC_FRAMES:
                #    self.TOTAL += 1

                # reset the eye frame counter
                self.COUNTER = 0

            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame
            cv2.putText(frame, "Blinks: {}".format(self.TOTAL), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # show the frame
        self.result.emit(frame)

    def plot(self):
        plt.plot(self.ctrs, self.lowerthresh)
        plt.plot(self.ctrs, self.upperthresh)
        plt.plot(self.ctrs, self. ar_est)
        plt.plot(self.ctrs, self.eyeopens)
        plt.show()

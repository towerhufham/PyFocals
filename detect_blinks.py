# USAGE
# python detect_blinks.py --shape-predictor shape_predictor_68_face_landmarks.dat --video blink_detection_demo.mp4
# python detect_blinks.py --shape-predictor shape_predictor_68_face_landmarks.dat

# import the necessary package/s
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
#import argparse
import imutils
import time
import dlib
import cv2

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
 
class FaceTracker(object):
	def __init__(self):
		# define two constants, one for the eye aspect ratio to indicate
		# blink and then a second constant for the number of consecutive
		# frames the eye must be below the threshold
		self.EYE_AR_THRESH = 0.195
		self.EYE_AR_CONSEC_FRAMES = 3

		# initialize the frame counters and the total number of blinks
		self.lCOUNTER = 0
		self.rCOUNTER = 0
		self.lTOTAL = 0
		self.rTOTAL = 0

		# initialize dlib's face detector (HOG-based) and then create
		# the facial landmark predictor
		print("[INFO] loading facial landmark predictor...")
		self.detector = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor(
			"shape_predictor_68_face_landmarks.dat")

		# grab the indexes of the facial landmarks for the left and
		# right eye, respectively
		(self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
		(self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

		# start the video stream thread
		# print("[INFO] starting video stream thread...")
		# vs = None
		# try:
		# 	vs = VideoStream(usePiCamera=False).start()
		# except:
		# 	vs = VideoStream(usePiCamera=True).start()
		# fileStream = False

		# time.sleep(1.0)

	def track(self, frame):
		# if this is a file video stream, then we need to check if
		# there any more frames left in the buffer to process

		# grab the frame from the threaded video file stream, resize
		# it, and convert it to grayscale
		# channels)

		#frame = vs.read()
		frame = imutils.resize(frame, width=450)
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


			# compute the convex hull for the left and right eye, then
			# visualize each of the eyes
			leftEyeHull = cv2.convexHull(leftEye)
			rightEyeHull = cv2.convexHull(rightEye)
			cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
			cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

			# check to see if the eye aspect ratio is below the blink
			# threshold, and if so, increment the blink frame counter
			if leftEAR < self.EYE_AR_THRESH:
				self.lCOUNTER += 1

			# otherwise, the eye aspect ratio is not below the blink
			# threshold
			else:
				# if the eyes were closed for a sufficient number of
				# then increment the total number of blinks
				if self.lCOUNTER >= self.EYE_AR_CONSEC_FRAMES:
					self.lTOTAL += 1
				# reset the eye frame counter
				self.lCOUNTER = 0

			if rightEAR < self.EYE_AR_THRESH:
				self.rCOUNTER += 1
			else:
				if self.rCOUNTER >= self.EYE_AR_CONSEC_FRAMES:
					self.rTOTAL += 1
				self.rCOUNTER = 0


			# draw the total number of blinks on the frame along with
			# the computed eye aspect ratio for the frame
			cv2.putText(frame, "LeftWinks: {}".format(self.lTOTAL), (10, 30),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			cv2.putText(frame, "RightWinks: {}".format(self.rTOTAL), (10, 60),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			cv2.putText(frame, "LeftEAR: {:.2f}".format(leftEAR), (270, 30),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			cv2.putText(frame, "RightEAR: {:.2f}".format(rightEAR), (270, 60),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

			print("LeftWinks: {};".format(self.lTOTAL),
			      "RightWinks: {}".format(self.rTOTAL))
	
		# show the frame
		# cv2.imshow("Frame", frame)
		# key = cv2.waitKey(1) & 0xFF
		return frame

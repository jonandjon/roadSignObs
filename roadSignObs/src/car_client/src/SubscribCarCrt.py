#!/usr/bin/env python

# Software License Agreement (BSD License)
# Copyright (c) 2018, jonas heinke j.h
# Empfaengt Strassenschild-Images und zugehoerige Labels
# Labels wurden von Prediction.py & Cnn.py ermittelt
# Die erkannten Verkehrsschilder beinflussen die Steuerung des Autos 

import numpy as np
# rospy for the subscriber
import rospy
from std_msgs.msg import String, Bool, Int32
# ROS Image message
from sensor_msgs.msg import Image, CompressedImage
## Importtyp (j.h)
## from sensor_msgs.msg import CompressedImage
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2
# j.h keras musste nachinstalliert werden
from keras.datasets import mnist
import tensorflow as tf
# Instantiate CvBridge
bridge = CvBridge()
# image
from PIL import Image
import time
import os
import csv ###

class SubscribCar:
	def __init__(self):
		self.cv_bridge = CvBridge()
		print("Subscribe image and prediction number (Konstruktor)")

		# Empfang prediction number
		self.subcribPredictionNumber=rospy.Subscriber(name='/camera/input/specific/number',
			data_class=Int32,
			callback=self.callbackRoadSignNumber,
			queue_size = 10) ## 
		

	## ----------------------------------------------------------------------------------------------
	def callbackRoadSignNumber(self, roadSignNumber):
		#-# subscribPredictionImage(callback_args=roadSignNumber)
		# Empfang road sign	
		self.subscribPredictionImage=rospy.Subscriber(name='camera/output/specific/compressed_img_msgs',
			data_class=CompressedImage,
			callback=self.CallbackRoadSignImage,
			callback_args=roadSignNumber,
			queue_size = 10)  
		
	def CallbackRoadSignImage(self, roadSignImage, roadSignNumber):
		#test#  rospy.loginfo(rospy.get_caller_id() + 'SubscribeImages heard %3s. %s ',str(roadSignNumber), roadSignImage.data)
		label=self.readReferenz(roadSignNumber)
		print("Label of the predicted road sign: %2d = %s" % (roadSignNumber.data, label))
		# print(str(num.data)+". "+picture.data) # zum TEST
		# Ausgabe als Bild
		np_arr = np.fromstring(roadSignImage.data, np.uint8)
		#+# image_np = cv2.imdecode(np_arr,  cv2.COLOR_RGB2HSV ) #cv2.CV_LOAD_IMAGE_COLOR #cv2.IMREAD_COLOR, cv2.COLOR_BGR2HSV, cv2.COLOR_BGR2GRAY
		image_np = cv2.imdecode(np_arr,  cv2.COLOR_RGB2HSV ) 
		cv2.imshow('cv_img', image_np)
		cv2.waitKey(1)
		
	# liest Bilddateien -----------------------------------
	def readReferenz(self, roadSignNumber):
		#label=""
		gtFile = open('nummerBezeichnungReferenz.csv', "r" ) # annotations file
		gtReader = csv.reader(gtFile, delimiter=',') # csv parser for annotations file, ## gtReader = csv.DictReader(gtFile, delimiter=';')
		gtReader.next() # skip header
		#gtReader.next() 
		label=''
		for row in gtReader:
			if roadSignNumber.data == int(row[0]):
				label= row[3]
		gtFile.close()
		return label	
		
		
		
	# -------------------------------------------------------------------------------------------------
def main():
	verbose = 0  # use 1 for debug

	# register node
	rospy.init_node('SubscribCar', anonymous=True)
	car=SubscribCar()
		
	try:
		rospy.spin()

	except KeyboardInterrupt:
		print "Shutting down ROS SubsciberCam"
	cv2.destroyAllWindows()
		
if __name__ == '__main__':
	main()  ##Subsrib Image and Number

#!/usr/bin/env python2.7
# coding: utf-8

# Node dedicated to the identification of cracks in images of the internal surface of the cave.


import rospy
import rospkg

import cv2
import numpy as np
import matplotlib.pyplot as plt

import glob
from skimage.morphology import skeletonize

def rgb_fissure_to_binary(image):
	grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	grey_img = cv2.GaussianBlur(grey_img, (3,3), 3)

	# ret,thresh = cv2.threshold(grey_img,11,255,cv2.THRESH_BINARY_INV)
	thresh = cv2.adaptiveThreshold(grey_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,2*(grey_img.shape[0]//42)+1,6)

	kernel = np.ones(2)
	cleaned_detection = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

	skeleton = (255*skeletonize(thresh==255)).astype(np.uint8)

	return skeleton


def run():

	####################    ROS initialisation     #########################
	######################################################################
	cv2.namedWindow('Origin', cv2.WINDOW_NORMAL)
	cv2.namedWindow('Test', cv2.WINDOW_NORMAL)
	rospy.init_node('imageProcessing', anonymous=True)

	rospy.loginfo("Launched identification node")

	r = rospkg.RosPack()
	package_path = r.get_path('projet_exploration')


	#################     Test images     ###############################
	#####################################################################
	images = glob.glob(package_path+'/test_images/*.png')

	for fname in images:
		origin_img = cv2.imread(fname)

		cleaned_detection = rgb_fissure_to_binary(origin_img)

		cv2.imshow('Origin', origin_img)
		cv2.imshow('Test', cleaned_detection)

		key = cv2.waitKey(0)
		if key & 0xFF == 27:
			break

	cv2.destroyAllWindows()










if __name__ == "__main__":
	run()
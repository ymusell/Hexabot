#!/usr/bin/env python2

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import cv2

from geometry_msgs.msg import Point

def binary_image_to_xyz(binary_image, depth_image):

	x,y,z = [],[],[]
	horizontal_fov = 1.047
	height, width = binary_image.shape
	d_theta = width/(2*horizontal_fov)
	for i in range(height):
		for j in range(width):
			if binary_image[i,j] == True:
				w = j-width//2
				h = -(i-height//2)
				d = depth_image[i,j]
				th_width = w/d_theta
				th_height = h/d_theta
				dxy = d*np.cos(th_height)
				z.append(d*np.sin(th_height))
				x.append(dxy*np.cos(th_width))
				y.append(-dxy*np.sin(th_width))

	return x,y,z

def color_image_to_binary_old(rgb_image,depth_image):
	gray = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(5,5),0)
	ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	return (gray > th3)

def color_image_to_binary(image):
    grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    grey_img = cv2.GaussianBlur(grey_img, (3,3), 3)

    # ret,thresh = cv2.threshold(grey_img,8,255,cv2.THRESH_BINARY_INV)
    thresh = cv2.adaptiveThreshold(grey_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,2*(grey_img.shape[0]//42)+1,6)

    kernel = np.ones(2)
    cleaned_detection = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    return (cleaned_detection == 0)


def publish_point_fissure(pub, marker, x,y,z):
	l_points = []
	for i in range(len(x)):
		p = Point()
		p.x = x[i]
		p.y = y[i]
		p.z = z[i]
		l_points.append(p)
	marker.points = l_points
	pub.publish(marker)




if __name__ == '__main__':
	rgb_image = np.load('rgb.npy')
	depth_image = np.load('depth.npy')
	plt.subplot('121')
	plt.imshow(rgb_image)
	plt.subplot('122')
	plt.imshow(depth_image)
	binary_image = color_image_to_binary(rgb_image)

	plt.imshow(binary_image);plt.show()

	x,y,z = binary_image_to_xyz(binary_image, depth_image)

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(x, y, z)

	ax.set_xlabel('X Label')
	ax.set_ylabel('Y Label')
	ax.set_zlabel('Z Label')

	plt.show()
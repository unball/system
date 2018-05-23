#!/usr/bin/env python

import rospy
from math import pi
from math import fabs
from math import isnan
from communication.msg import robots_speeds_msg
from communication.msg import wheels_speeds_msg

msg = comm_msg()
number_of_robots = 3

convertion = (512*19) / 100
wheel_reduction = 3/ 1
r = 0.03
L = 0.075

max_tics_per_s = 70000.
encoder_resolution = 512.*19
max_motor_speed = (max_tics_per_s) / encoder_resolution

number_of_robots = 3

class speed:
	def __init__(self):
		self.right = 0
		self.left = 0

	def divideEachSide(self, value):
		self.right = self.right/value
		self.left = self.left/value

	def multiplyEachSide(self,value):
		self.right = self.right*value
		self.left = self.left*value		


def normalize(w1, w2):
	if fabs(w1) >= fabs(w2):
		w2 = max_motor_speed * w2/fabs(w1)
		w1 = max_motor_speed * w1/fabs(w1)
	elif fabs(w2) >= fabs(w1):
		w1 = max_motor_speed * w1/fabs(w2)
		w2 = max_motor_speed * w2/fabs(w2)

	return w1, w2	


def speeds2motors(robot):
		wheels = speed()
		wheels.right = (-robot.u + (L/2)*robot.w) / r
		wheels.left = (-robot.u - (L/2)*robot.w) / r
		wheels.divideEachSide(2*pi)

		if fabs(wheels.right) > max_motor_speed or fabs(wheels.left) > max_motor_speed:
			motor_rotations1, motor_rotations2 = normalize(motor_rotations1, motor_rotations2)

		wheels.multiplyEachSide(convertion)
		return wheels.right, wheels.left


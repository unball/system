#!/usr/bin/env python
import math
from pose_control import *
from position_control import *
from curve_control import *
from control_options import *

number_of_robots = 3

def controller(robot):
	orientation = copysign(1,robot.u)

	if robot.control ==  control_options.pose:
		u,w = pose_control(robot)

	elif robot.control == control_options.curve:
		u,w = curve_control(robot)

	elif robot.control == control_options.spinCCW:
		u = 0
		w = 15

	elif robot.control == control_options.spinCW:
		u = 0
		w = -15

	elif robot.control == control_options.fullSteam:
		if orientation > 0:
			u = 0.5
		else:
			u = -0.5

		w = 0

	else:
		u,w = position_control(robot)

	return u, w

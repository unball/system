import rospy
from communication.msg import target_positions_msg
from communication.msg import robots_speeds_msg
from math import *
from control_utils import *

orientation = 1


def position_control(robot):
	relative_target = convertTargetPositions(robot)

	if relative_target[1] > 0:
		orientation = 1
	else:
		orientation = -1

	error_angle = calculateErrorAngle(relative_target,orientation)
	error_magnitude = calculateDistance(relative_target)

	print error_angle

	u = robot.k_u * error_magnitude * orientation * (cos(error_angle))
	w = robot.k_w * error_angle

	return u, w
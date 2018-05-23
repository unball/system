import rospy
from communication.msg import target_positions_msg
from communication.msg import robots_speeds_msg
from math import *
from control_utils import *

def pose_control(robot):
	relative_target = convertTargetPositions(robot)

	if relative_target[1] > 0:
		orientation = 1
	else:
		orientation = -1

	error_angle = calculateErrorAngle(relative_target,orientation)
	error_magnitude = calculateDistance(relative_target)

	u = robot.k_u * error_magnitude * orientation * (cos(error_angle))
	w = robot.k_w * error_angle

	tolerance = 0.1

	if error_magnitude > tolerance:
		return u, w
	else:
		return 0, angdiff(robot.th, robot.dth)*robot.k_w
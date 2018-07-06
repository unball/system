import rospy
from communication.msg import target_positions_msg
from communication.msg import robots_speeds_msg
from math import *
from control_utils import *

orientation = 1
i_error_distance = [[],[],[]]
i_error_angle = [[],[],[]]
integral_distance = [0,0,0]
integral_angle = [0,0,0]
magnitude_anterior = 0

def position_control(robot):
	global i_error_distance

	relative_target = convertTargetPositions(robot)

	if relative_target[1] > 0:
		orientation = 1
	else:
		orientation = -1

	error_angle = calculateErrorAngle(relative_target,orientation)
	error_magnitude = calculateDistance(relative_target)

	if len(i_error_distance[robot.id]) > 10000:
		del i_error_distance[robot.id][0]
		del i_error_angle[robot.id][0]

	i_error_distance[robot.id].append(error_magnitude)
	i_error_angle[robot.id].append(error_angle)
	integral_distance[robot.id] = sum(i_error_distance[robot.id])
	integral_angle[robot.id] = sum(i_error_distance[robot.id])

	if error_magnitude > 0.15:
		u = orientation*0.6*cos(error_angle)
	else:
		u = (robot.kp_u * error_magnitude+ robot.ki_u*integral_distance[robot.id])*orientation*cos(error_angle)

	if error_magnitude < 0.07:
		u = 0
		w = 0



	w = robot.kp_w * error_angle + robot.ki_w*integral_angle[robot.id]

	return u, w

import rospy
from communication.msg import target_positions_msg
from communication.msg import robots_speeds_msg
from math import *
from Robot import *
import numpy as np

orientation = 1
robot = Robot()

def convertLocalTarget(local_target,robot):
    relative_target = [local_target[0] - robot.x, local_target[1] - robot.y]
    relative_target = convertAxisToRobot(relative_target, robot.th)
    return relative_target

def convertAxisToRobot(vector, th):
 	ax = vector[0]
	ay = vector[1]
	y = ax*cos(th) + ay*sin(th)
	x = ax*sin(th) - ay*cos(th)
	return [x,y]

def drawLine(x,y,angle):
	m = tan(angle)
	n = y - x * m
	return m,n

def findIntersection(line1, line2):
	print(line1,line2)
	a = np.array([[-line1[0] , 1] , [-line2[0], 1]])
	b = np.array([line1[1] , line2[1]])
	print(a,b)
	intersection = np.linalg.solve(a,b)
	return intersection

def findMiddlePoint(p,q,alpha):
	x = (alpha*p[0] + (1-alpha)*q[0])
	y = (alpha*p[1] + (1-alpha)*q[1])
	return [x,y]

def findLocalTarget(robot,alpha):
	robot_line = drawLine(robot.x,robot.y,robot.th)
	desired_line = drawLine(robot.dx,robot.dy,robot.th)
	intersection = findIntersection(robot_line,desired_line)
	middle_point = findMiddlePoint([robot.x, robot.y],[robot.dx, robot.dy],0.5)
	target = findMiddlePoint(middle_point,intersection,alpha)
	return target

def calculateErrorAngle(vector, orientation):
 	if vector == [0,0]:
 		th = 0
 	else:
 		th = atan2(-orientation*vector[0], orientation*vector[1])
 	return (th)

def calculateDistance(vector):
	return (sqrt(vector[0]**2 + vector[1]**2))

def curve_control(robot):
	local_target = findLocalTarget(robot, 0.8)
	relative_vector = convertLocalTarget(local_target,robot)
	orientation = copysign(1,relative_vector[1])

	error_angle = calculateErrorAngle(local_target,orientation)
	error_magnitude = calculateDistance(local_target)

	u = robot.k_u * error_magnitude * orientation * (cos(error_angle))
	w = robot.k_w * error_angle

	return u,w


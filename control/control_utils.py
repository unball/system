from math import *

def convertTargetPositions(robot):
    relative_target = [robot.dx - robot.x, robot.dy - robot.y]
    relative_target = convertAxisToRobot(relative_target, robot.th)
    return relative_target

def convertAxisToRobot(vector, th):
 	ax = vector[0]
	ay = vector[1]
	y = ax*cos(th) + ay*sin(th)
	x = ax*sin(th) - ay*cos(th)
	return [x,y]

def calculateErrorAngle(vector, orientation):
 	if vector == [0,0]:
 		th = 0
 	else:
 		th = atan2(-orientation*vector[0], orientation*vector[1])
 	return (th)

def calculateDistance(vector):
	return (sqrt(vector[0]**2 + vector[1]**2))

def angdiff_180(robot_angle,desired_angle):
	return ((robot_angle - desired_angle + pi/2) % (pi)) - pi/2

def angdiff(robot_angle,desired_angle):
	#Difference between two angles, the result wrapped on the interval [-pi,pi].
	return ((robot_angle - desired_angle + pi) % (2*pi)) - pi
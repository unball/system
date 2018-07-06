from control_options import *
from math import *
import planar
import numpy as np
import time

global t
t = 0
def defender(robot,ball):
	distance2ball = sqrt((robot.x-ball.x)**2 + (robot.y - ball.y)**2)
	x = ball.x
	y = ball.y
	th = 0
	if distance2ball < 0.075:
		if (ball.side == -1 and ballUpRobot(ball,robot)) or (ball.side == 1 and not(ballUpRobot(ball,robot))):
			control = control_options.spinCCW
		else:
			control = control_options.spinCW
	else:
		control = control_options.position

	if ball.side == 1:
		if x < -ball.side*0.55:
			x = -ball.side*0.55
		elif x > ball.side*0.05:
			x = ball.side*0.05
	else:
		if x > -ball.side*0.55:
			x = -ball.side*0.55
		elif x < ball.side*0.05:
			x = ball.side*0.05

	return control, x, y, th

def rightSide(robot,ball):
	distance2right = abs((0.75*ball.side)-ball.x)
	distance2wrong = abs((0.75*ball.side)-robot.x)

	return(distance2wrong>distance2right)

def ballUpRobot(robot,ball):
	return (robot.y>ball.y)

def lookingAtWrongGoal(robot,ball):
	y_wall = (0.65*ball.side)*tan(robot.th) - tan(robot.x)*robot.x + robot.y

	return (abs(y_wall)<0.2)

def timeToStop(start):
	return(time.time() - start > 1)

	


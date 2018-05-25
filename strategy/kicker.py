from control_options import *
from math import *

def kicker(robot,ball):
	distance2ball = sqrt((robot.x-ball.x)**2 + (robot.y - ball.y)**2)
	x = ball.x
	y = ball.y
	th = 0
	if distance2ball < 0.05:
		if ball.side == 0:
			control = control_options.spinRight
		else:
			control = control_options.spinLeft
	else:
		control = control_options.position


	return control, x, y, th
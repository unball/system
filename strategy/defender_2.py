from control_options import *

def defender2(robot,ball):
	x = ball.x
	y = ball.y
	th = 0.1
	if ball.side == 1:
		if x < -ball.side*0.55:
			x = -ball.side*0.55
		elif x > ball.side*0.3:
			x = ball.side*0.3
	else:
		if x > -ball.side*0.55:
			x = -ball.side*0.55
		elif x < ball.side*0.3:
			x = ball.side*0.3
	control = control_options.position
	return control, x, y, th

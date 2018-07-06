from control_options import *

def updated_gtb(robot,ball):
	x = ball.x
	y = ball.y
	th = 0.1
	control = control_options.position
	if ball.side == 1:
		if x < -ball.side*0.55:
			x = -ball.side*0.55
	else:
		if x > -ball.side*0.55:
			x = -ball.side*0.55
	return control, x, y, th

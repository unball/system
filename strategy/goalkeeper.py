import math as m

def goalkeeper(robot,ball):
	x = ball.side*0.6
	if (abs(ball.y) > .2):
		y = .2
	else:
		y = ball.y

	control = control_options.position
	th = 0
	return control, x, y, th
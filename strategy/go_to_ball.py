from control_options import *

def go_to_ball(robot,ball):
	x = .5
	y = .5
	th = 0.1
	control = control_options.position
	return control, x, y, th

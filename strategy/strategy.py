import math as m
from control_options import *
from go_to_ball import *
from test import *
from kicker import *

def start(robot, ball):
	if robot.strategy == "kicker":
		control,x,y,th = kicker(robot,ball)
	else:
		control,x,y,th = go_to_ball(robot,ball)

	return control,x,y,th
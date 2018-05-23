import math as m
from control_options import *
from go_to_ball import *
from test import *

def start(robot, ball):
	control,x,y,th = go_to_ball(robot,ball)

	return control,x,y,th
import math as m
from control_options import *
from go_to_ball import *
from test import *
from kicker import *
from olympic_lap import *
from goalkeeper import *
from test import *

def start(robot, ball):
	if robot.strategy == "kicker":
		control,x,y,th = kicker(robot,ball)
	elif robot.strategy == "olympic_lap":
		control, x, y, th = olympic_lap(robot)
	elif robot.strategy == "test":
		control,x,y,th = test(robot)
	elif robot.strategy == "goalkeeper":
		control, x, y, th = goalkeeper(robot,ball)
	else:
		control,x,y,th = go_to_ball(robot,ball)



	return control,x,y,th
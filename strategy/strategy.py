import math as m
from control_options import *
from go_to_ball import *
from test import *
from kicker import *
from olympic_lap import *
from goalkeeper import *
from test import *
from updated_gtb import *
from defender import *
from defender_2 import *
from new_attack import *

def start(robot, ball):
	if robot.strategy == "kicker":
		control,x,y,th = kicker(robot,ball)
	elif robot.strategy == "olympic_lap":
		control, x, y, th = olympic_lap(robot)
	elif robot.strategy == "test":
		control,x,y,th = test(robot)
	elif robot.strategy == "goalkeeper":
		control, x, y, th = goalkeeper(robot,ball)
	elif robot.strategy == 'updated_gtb':
		control, x, y, th = updated_gtb(robot,ball)
	elif robot.strategy == 'defender2':
		control, x, y, th = defender2(robot,ball)
	elif robot.strategy == 'defender':
		control, x, y, th = defender(robot,ball)
	elif robot.strategy == 'new_attack':
		control,x,y,th = new_attack(robot,ball)
	else:
		control,x,y,th = go_to_ball(robot,ball)

	return control,x,y,th
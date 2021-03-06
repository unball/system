from control_options import *
import time

start = []

def test(robot):
	start.append(time.time())
	if len(start)>1:
		del start[1]

	points = 0.4

	if(robot.dy == points and robot.dx == points):
		next_target_x = -points
		next_target_y = points
	elif(robot.dy == points and robot.dx == -points):
		next_target_x = -points
		next_target_y = -points
	elif(robot.dy == -points and robot.dx == -points):
		next_target_y = -points
		next_target_x = points
	elif(robot.dy == -points and robot.dx == points):
		next_target_y = points
		next_target_x = points
	else:
		y = points
		x = points
		next_target_x = points
		next_target_y = points
	
	if(time.time() - start[0])>4:
		x = next_target_x
		y = next_target_y
		start[0] = time.time()

	else:
		x = robot.dx
		y = robot.dy

	th = 0
	control = control_options.position
	return control,x,y,th
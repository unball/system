from control_options import *

def olympic_lap(robot):

	points = 0.3

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
	
	if(abs(robot.y - robot.dy) <=0.1 and abs(robot.x - robot.dx) <=0.1):
		x = next_target_x
		y = next_target_y

	else:
		x = robot.dx
		y = robot.dy

	th = 0
	control = control_options.position
	return control,x,y,th
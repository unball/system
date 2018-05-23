#!/usr/bin/env python

from Robot import Robot
from Ball import Ball
import rospy
from strategy.strategy import *
from sensor_msgs.msg import Joy
from control.control import *
from communication.msg import robots_speeds_msg
from measurement_system.msg import measurement_msg
from communication.msg import comm_msg
from speed_conversion.speed_converter import *
from joystick.joystick import *

number_of_robots = 3
robots = []
control_constants = [[0.5,5],[0.5,5],[0.5,5]]
speeds = robots_speeds_msg()
motors = comm_msg()
strategies = ["test","go_to_ball","go_to_ball"]
joystick = [True, True, True]

def system(data):
	ball = Ball()
	ball.x = data.ball_x
	ball.y = data.ball_y
	ball.pred_x = data.ball_x_pred
	ball.pred_y = data.ball_y_pred
	ball.walls_x = data.ball_x_walls
	ball.walls_y = data.ball_y_walls
	for i in range(number_of_robots):
		robot = Robot()
		if not(joystick[i]):
			robot.id = i
			robot.x = data.x[i]
			robot.y = data.y[i]
			robot.th = data.th[i]
			robot.k_u = control_constants[i][0]
			robot.k_w = control_constants[i][1]
			robot.strategy = strategies[i]
			robot.control, robot.dx, robot.dy, robot.dth = start(robot, ball)
			robot.u, robot.w = controller(robot)
			motors.MotorA[i], motors.MotorB[i] = speeds2motors(robot)
			speeds.linear_vel[i], speeds.angular_vel[i] = controller(robot)



def receive_joystick(data):
	for i in range(number_of_robots):
		if joystick[i]:
			speeds.linear_vel[i], speeds.angular_vel[i] = joystick_control(data)
			robot.u, robot.w = speeds.linear_vel[i], speeds.angular_vel[i]
			motors.MotorA[i], motors.MotorB[i] = speeds2motors(robot)

def main():
	print 'planning node started'

	rospy.init_node('planning_node')
	pub1 = rospy.Publisher('robots_speeds', robots_speeds_msg, queue_size=1)
	pub2 = rospy.Publisher('radio_topic',comm_msg,queue_size=1)

	rospy.Subscriber('measurement_system_topic', measurement_msg, system)
	if any(joystick):
		rospy.Subscriber('joy',Joy,receive_joystick)

	rate = rospy.Rate(30)	
	try:
		while not rospy.is_shutdown():
			pub1.publish(speeds)
			pub2.publish(motors)
			rate.sleep()
	except rospy.ROSInterruptException:
		exit(1)


if __name__ == '__main__':
	main()

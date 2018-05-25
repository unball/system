#!/usr/bin/env python

from Robot import Robot
from Ball import Ball
import rospy
from strategy.strategy import *
from sensor_msgs.msg import Joy
from control.control import *
from communication.msg import robots_speeds_msg
from vision.msg import VisionMessage
from communication.msg import comm_msg
from speed_conversion.speed_converter import *
from joystick.joystick import *
from measurement_system.measurement import *

number_of_robots = 3
robot = [Robot(), Robot(), Robot()]
control_constants = [[0.2,1],[0.2,1],[0.2,1]]
speeds = robots_speeds_msg()
motors = comm_msg()
strategies = ["kicker","go_to_ball","go_to_ball"]
joystick = [False, False, False]

def system(data):
	ball = Ball()
	ball.x = data.ball_x
	ball.y = data.ball_y
	for i in range(3):
		if not(joystick[i]):
			robot[i].id = i
			robot[i].x = data.x[i]
			robot[i].y = data.y[i]
			robot[i].th = data.th[i]
			robot[i].k_u = control_constants[i][0]
			robot[i].k_w = control_constants[i][1]
			robot[i].strategy = strategies[i]
			robot[i].control, robot[i].dx, robot[i].dy, robot[i].dth = start(robot[i], ball)
			robot[i].u, robot[i].w = controller(robot[i])
			motors.MotorA[i], motors.MotorB[i] = speeds2motors(robot[i])
			speeds.linear_vel[i], speeds.angular_vel[i] = controller(robot[i])



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

	rospy.Subscriber('pixel_to_metric_conversion_topic', VisionMessage, system)
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

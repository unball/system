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
import time

number_of_robots = 3
robot = [Robot(), Robot(), Robot()]
k_p = [[0.1,1],[1,1],[0.2,1]]
k_i = [[0.1,0],[0,0],[0,0]]
k_d = [[0.1,0],[0,0],[0,0]]
speeds = robots_speeds_msg()
motors = comm_msg()
strategies = ["go_to_ball","go_to_ball","go_to_ball"]
joystick = [False, False, False]
#cont = 0
#total_time = 0
#myfle = open("time.txt",'a+')

def writeInFile(robot):
	files = ['robot1.txt','robot2.txt','robot3.txt']
	for i in range(3):
		myfile = open(files[i], 'a+')
		myfile.write('%f,%f,%f,%f,%f\n'%(robot[i].dx,robot[i].dy,robot[i].dth,robot[i].u,robot[i].w))

def system(data):
#	global total_time
#	global cont
	start_time = time.time()
	ball = Ball()
	ball.x = data.ball_x
	ball.y = data.ball_y
	for i in range(3):
		if not(joystick[i]):
			robot[i].id = i
			robot[i].x = data.x[i]
			robot[i].y = data.y[i]
			robot[i].th = data.th[i]
			robot[i].kp_u = k_p[i][0]
			robot[i].kp_w = k_p[i][1]
			robot[i].ki_u = k_i[i][0]
			robot[i].ki_w = k_i[i][1]
			robot[i].kd_u = k_d[i][0]
			robot[i].kd_w = k_d[i][1]
			robot[i].strategy = strategies[i]
			robot[i].control, robot[i].dx, robot[i].dy, robot[i].dth = start(robot[i], ball)
			robot[i].u, robot[i].w = controller(robot[i])
			motors.MotorA[i], motors.MotorB[i] = speeds2motors(robot[i])
			speeds.linear_vel[i], speeds.angular_vel[i] = controller(robot[i])

#	writeInFile(robot)
#	cont +=1
#	processing_time = time.time() - start_time
#	total_time = total_time + processing_time
#	myfle.write('%f\n'%(processing_time))
#	print("Processing time: %f"%(processing_time))
#	print("Average processing time: %f"%(total_time/cont))





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

	rospy.Subscriber('vision_output_topic', VisionMessage, system)
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

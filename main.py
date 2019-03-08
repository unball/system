#!/usr/bin/env python
from Robot import Robot
from Ball import Ball
from std_msgs.msg import String
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
k_p = [[1,2],[1,2],[0.5,0.5]]
k_i = [[0,0],[0,0],[0,0]]
k_d = [[0,0],[0,0],[0,0]]
speeds = robots_speeds_msg()
motors = comm_msg()
strategies = ["goalkeeper","goalkeeper","new_attack"]
joystick = [False, False, False]
paused = False
ball = Ball()

def writeInFile(robot):
    files = ['robot1.txt','robot2.txt','robot3.txt']
    for i in range(3):
        myfile = open(files[i], 'a+')
        myfile.write('%f,%f,%f,%f,%f\n'%(robot[i].dx,robot[i].dy,robot[i].dth,robot[i].u,robot[i].w))

def keyboardReceiver(data):
    global paused
    data.data = data.data.lower()
    if data.data == "r":
        ball.side = 1
    elif data.data == "l":
        ball.side = -1

    if data.data == "p":
        paused = True
    if data.data == "g":
        paused = False

def system(data):
    start_time = time.time()
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


#   writeInFile(robot)

def receive_joystick(data):
    for i in range(number_of_robots):
        if joystick[i]:
            speeds.linear_vel[i], speeds.angular_vel[i] = joystick_control(data)
            robot[i].u, robot[i].w = speeds.linear_vel[i], speeds.angular_vel[i]
            motors.MotorA[i], motors.MotorB[i] = speeds2motors(robot[i])

def main():
    print 'planning node started'

    rospy.init_node('planning_node')
    pub1 = rospy.Publisher('robots_speeds', robots_speeds_msg, queue_size=1)
    pub2 = rospy.Publisher('radio_topic',comm_msg,queue_size=1)

    rospy.Subscriber('vision_output_topic', VisionMessage, system)
    if any(joystick):
        rospy.Subscriber('joy',Joy,receive_joystick)
    rospy.Subscriber('keyboard_topic',String,keyboardReceiver)
    rate = rospy.Rate(30)

    try:
        while not rospy.is_shutdown():
            if paused:
                for i in range(3):
                    motors.MotorA[i] = 0
                    motors.MotorB[i] = 0

            pub1.publish(speeds)
            pub2.publish(motors)
            rate.sleep()
    except rospy.ROSInterruptException:
        exit(1)


if __name__ == '__main__':
    main()

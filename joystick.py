import rospy
from Robot import Robot
from communication.msg import comm_msg
from speed_conversion.speed_converter import *
from sensor_msgs.msg import Joy

robot = Robot()
msg = comm_msg()
global speed
global ang
def callback(data):
    f = -(1 - data.axes[2])
    b = -(1 - data.axes[5])
    robot.u = (f - b)*.25
    robot.w = data.axes[0]*3
    if data.buttons[0]:
        robot.u = 0
        robot.w = 15

    for i in range(3):
        msg.MotorA[i], msg.MotorB[i] = speeds2motors(robot)
            
    
    

rospy.init_node('JoyRobot')
pub = rospy.Publisher('radio_topic',comm_msg,queue_size=1)
rospy.Subscriber('joy',Joy,callback)
rate = rospy.Rate(30)

while not rospy.is_shutdown():
    pub.publish(msg)
    rate.sleep()
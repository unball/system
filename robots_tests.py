import rospy
from communication.msg import comm_msg
from std_msgs.msg import String

motors = comm_msg()
paused = False

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

def main():
    print 'test started'

    rospy.Subscriber('keyboard_topic',String,keyboardReceiver)
    rospy.init_node('test_robots')
    pub = rospy.Publisher('radio_topic',comm_msg,queue_size=1)
    rate = rospy.Rate(30)

    try:
        while not rospy.is_shutdown():
            motors.MotorA[0] = -50
            motors.MotorB[0] = 50
            motors.MotorA[1] = -350
            motors.MotorB[1] = 350
            motors.MotorA[2] = 650
            motors.MotorB[2] = -650

            while not paused:            
                pub.publish(motors)
            
            rate.sleep()
    except rospy.ROSInterruptException:
        exit(1)

if __name__ == '__main__':
    main()
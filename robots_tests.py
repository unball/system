import rospy
from communication.msg import comm_msg
motors = comm_msg()

def main():
    print 'test started'

    rospy.init_node('test_robots')
    pub = rospy.Publisher('radio_topic',comm_msg,queue_size=1)
    rate = rospy.Rate(30)

    try:
        while not rospy.is_shutdown():
            motors.MotorA[0] = 0
            motors.MotorB[0] = 0
            motors.MotorA[1] = 0
            motors.MotorB[1] = 00
            motors.MotorA[2] = 100
            motors.MotorB[2] = 100            
            pub.publish(motors)
            rate.sleep()
    except rospy.ROSInterruptException:
        exit(1)

if __name__ == '__main__':
    main()
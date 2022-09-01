#!/usr/bin/env python3

import rospy
import turtlesim.msg
from geometry_msgs.msg import Twist


x2 = 0
y2 = 0

def sub_callback(data):
	global x2, y2
	x2 = data.x
	y2 = data.y


def turtle_circle():
    rospy.init_node('turtlesim', anonymous=True)
    rospy.Subscriber("/turtle1/pose",turtlesim.msg.Pose,sub_callback)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)
    vel = Twist()

    while not rospy.is_shutdown():
        vel.linear.x = 2
        vel.linear.y = 0
        vel.linear.z = 0
        vel.angular.x = 0
        vel.angular.y = 0
        vel.angular.z = 1
        location = "x = %2.2f\ny = %2.2f\n\n" % (x2,y2)
        rospy.loginfo(location)

        pub.publish(vel)
        rate.sleep()


if __name__ == '__main__':
    try:
        turtle_circle()
    except rospy.ROSInterruptException:
        pass

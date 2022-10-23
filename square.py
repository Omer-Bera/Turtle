#!/usr/bin/env python3

import rospy
import turtlesim.msg
from geometry_msgs.msg import Twist
PI = 3.1415926535897

x2 = 0
y2 = 0

global edge
edge = 0

def sub_callback(data):
	global x2, y2
	x2 = data.x
	y2 = data.y

def turtle_edge(vel,pub,r,edge):
    current_x = x2
    current_y = y2
    aim_x = x2
    aim_y = y2
    speed = 4.0
    edge_l = 4.0
    edge = edge % 4
    vel.linear.x = 0.0
    vel.linear.y = 0.0
    if (edge % 2 == 0):
        if (edge == 0):
            aim_x = current_x + edge_l
            vel.linear.x = speed
            while((current_x < aim_x) and (not rospy.is_shutdown())):
                current_x = x2
                location = "x = %2.2f\ny = %2.2f\n\n" % (x2,y2)
                rospy.loginfo(location)
                pub.publish(vel)
                r.sleep()
            vel.linear.x = 0.0
            pub.publish(vel)
        else:
            aim_x = current_x - edge_l
            vel.linear.x = -1*(speed)
            while((current_x > aim_x) and (not rospy.is_shutdown()) ):
                location = "x = %2.2f\ny = %2.2f\n\n" % (x2,y2)
                current_x = x2
                rospy.loginfo(location)
                pub.publish(vel)
                r.sleep()
            vel.linear.x = 0.0
            pub.publish(vel)
    else:
        if (edge == 1):
            aim_y = current_y + edge_l
            vel.linear.y = speed
            while((current_y < aim_y) and (not rospy.is_shutdown()) ):
                location = "x = %2.2f\ny = %2.2f\n\n" % (x2,y2)
                current_y = y2
                rospy.loginfo(location)

                pub.publish(vel)
                r.sleep()
            vel.linear.y = 0.0
            pub.publish(vel)
        else:
            aim_y = current_y - edge_l
            vel.linear.y = -1*(speed)
            while((current_y > aim_y) and (not rospy.is_shutdown()) ):
                location = "x = %2.2f\ny = %2.2f\n\n" % (x2,y2)
                current_y = y2
                rospy.loginfo(location)

                pub.publish(vel)
                r.sleep()
            vel.linear.y = 0.0
            pub.publish(vel)
    
def turtle_square():
    rospy.init_node('turtlesim', anonymous=True)
    rospy.Subscriber("/turtle1/pose",turtlesim.msg.Pose,sub_callback)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1000)
    r = rospy.Rate(10)
    vel = Twist()
    edge = 0
    while not rospy.is_shutdown():
        edge_c = edge
        while(edge_c == edge):
            turtle_edge(vel,pub,r,edge)
            edge = edge + 1
            r.sleep()
        r.sleep()

if __name__ == '__main__':
    try:
        turtle_square()
    except rospy.ROSInterruptException:
        pass

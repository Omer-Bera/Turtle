#!/usr/bin/env python3

import rospy
import turtlesim.msg
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute

PI = 3.1415926535897

x2 = 0
y2 = 0
theta = 0

global edge
edge = 0

def sub_callback(data):
    global x2, y2, theta
    x2 = data.x
    y2 = data.y
    theta = data.theta

def turtle_edge(vel,pub,r,R,edge,telep):
    r.sleep()
    current_x = x2
    current_y = y2
    current_theta = theta
    aim_x = x2
    aim_y = y2
    speed = 4.0
    edge_l = 4.0
    edge = edge % 4
    vel.linear.x = 0.0
    vel.linear.y = 0.0
    vel.angular.z = 0.0
    if(edge % 2 == 0):
        if(edge == 0):
            aim_x = current_x + edge_l
        else:
            aim_x = current_x - edge_l
    else:
        if(edge == 1):
            aim_y = current_y + edge_l
        else:
            aim_y = current_y - edge_l
    vel.linear.x = speed
    while((abs(current_x - aim_x) + abs(current_y - aim_y) > 0.1  ) and (not rospy.is_shutdown()) ):
        current_x = x2
        current_y = y2
        location = "x = %2.2f\ny = %2.2f\n\n" % (x2,y2)
        aim = "aim_x = %2.2f\naim_y = %2.2f\n\n" % (aim_x, aim_y)
        rospy.loginfo(location)
        rospy.loginfo(aim)
        rospy.loginfo("vel.linear.x = %2.2f\n\n distance: %2.2f" % (vel.linear.x, abs(current_x - aim_x) + abs(current_y - aim_y)))
        pub.publish(vel)
        R.sleep()
    vel.linear.x = 0.0
    pub.publish(vel)
    telep.call(x = aim_x, y = aim_y, theta = current_theta)
    while( ( abs(abs(theta) - abs(current_theta + PI/2)) > 0.1) and (not rospy.is_shutdown()) ):
        vel.angular.z = 1.25
        angular = "theta = %2.2f \n current_theta + PI/2 = %2.2f" % (theta, current_theta + PI/2)
        rospy.loginfo(angular)
        pub.publish(vel)
        R.sleep()
    vel.angular.z = 0.0
    pub.publish(vel)
    telep.call(x= aim_x, y = aim_y, theta = current_theta + PI/2)

    
def turtle_square():
    rospy.init_node('turtlesim', anonymous=True)
    rospy.Subscriber("/turtle1/pose",turtlesim.msg.Pose,sub_callback)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=1000)
    telep = rospy.ServiceProxy("/turtle1/teleport_absolute", TeleportAbsolute)

    r = rospy.Rate(10)
    R = rospy.Rate(100)
    vel = Twist()
    edge = 0
    while not rospy.is_shutdown():
        edge_c = edge
        while(edge_c == edge):
            turtle_edge(vel,pub,r,R,edge,telep)
            edge = edge + 1
            r.sleep()
        r.sleep()

if __name__ == '__main__':
    rospy.wait_for_service("/turtle1/teleport_absolute")
    try:
        turtle_square()
    except rospy.ROSInterruptException:
        pass

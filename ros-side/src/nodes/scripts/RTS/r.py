#!/usr/bin/env python2
# _*_ coding: utf-8 _*_

import sys

import rospy
from geometry_msgs.msg import Twist


def move_ball(r_name):
	rospy.init_node('r', anonymous=True)

	pub = rospy.Publisher(r_name + '/twist', Twist, queue_size=3)

	rate = rospy.Rate(10)

	vel = Twist()

	while not rospy.is_shutdown():
		vel.linear.x = 10
		vel.linear.y = 0
		vel.linear.z = 0

		vel.angular.x = 0
		vel.angular.y = 0
		vel.angular.z = 0

		pub.publish(vel)

		rate.sleep()


if __name__ == '__main__':
	try:
		move_ball(sys.argv[1])
	except rospy.ROSInternalException:
		pass

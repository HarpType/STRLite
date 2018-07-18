#!/usr/bin/env python2
# _*_ coding: utf-8 _*_

import sys

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose2D


def move_ball(r_name):
	pass

if __name__ == '__main__':
	try:
		move_ball(sys.argv[1])
	except rospy.ROSInternalException:
		pass

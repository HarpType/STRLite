#!/usr/bin/env python2
# _*_ coding: utf-8 _*_

import sys

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose2D

old_ball_position = None
ball_position = None


def pos_callback(msg):
	global ball_position
	global old_ball_position

	old_ball_position = ball_position
	ball_position = (msg.x, msg.y)


def move_ball(r_name):
	rospy.init_node('r', anonymous=True)

	pub = rospy.Publisher(r_name + '/velocity', Twist, queue_size=3)
	rospy.Subscriber(r_name + '/position', Pose2D, pos_callback)

	rate = rospy.Rate(10)

	vel = Twist()

	course = -1
	change_tick = 0
	flag = False
	eps = 1.5
	while not rospy.is_shutdown():
		if old_ball_position:
			if abs(old_ball_position[0] - ball_position[0]) < eps:
				change_tick += 1
			else:
				if not flag:
					change_tick += 1
				else:
					change_tick = 0

			if flag:
				if change_tick > 0:
					course *= -1
					change_tick = 0
			else:
				if change_tick > 20:
					change_tick = 0
					flag = True

		vel.linear.x = 150 * course
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

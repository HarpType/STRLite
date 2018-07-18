#!/usr/bin/env python2
# _*_ coding: utf-8 _*_

import sys

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose2D
import math

target = (500, 200)
velocity = 60
normal_vector = None
stop = False
eps = 5


def pos_callback(msg):
	global stop
	global normal_vector
	robot_position = (msg.x, msg.y)
	vector = (target[0]-robot_position[0], target[1]-robot_position[1])
	if abs(vector[0]) < eps and abs(vector[1]) < eps:
		stop = True

	length = math.sqrt(vector[0]**2 + vector[1]**2)
	normal_vector = (vector[0]/length, vector[1]/length)


def move_ball(r_name):
	rospy.init_node('r', anonymous=True)

	pub = rospy.Publisher(r_name + '/velocity', Twist, queue_size=3)
	rospy.Subscriber(r_name + '/position', Pose2D, pos_callback)

	rate = rospy.Rate(10)

	vel = Twist()

	while not rospy.is_shutdown():
		while not normal_vector:
			pass

		if not stop:
			vel.linear.x = velocity * normal_vector[0]
			vel.linear.y = velocity * normal_vector[1]
			vel.linear.z = 0

			vel.angular.x = 0
			vel.angular.y = 0
			vel.angular.z = 0

			pub.publish(vel)
		else:
			vel.linear.x = 0
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

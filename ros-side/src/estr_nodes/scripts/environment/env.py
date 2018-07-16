#!/usr/bin/env python2

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

import sys
import json

import pymunk


mass = 1
radius = 14

moment = pymunk.moment_for_circle(mass, 0, radius)
body = pymunk.Body(mass, moment)

body.position = (50, 300)
body.velocity = (0, 0)
shape = pymunk.Circle(body, radius)
shape.friction = 0.5



def ball_callback(msg):
	global body

	# rospy.loginfo(msg.linear.x)
	body.velocity = (float(msg.linear.x), 0)


def init_ros(env_name):
	rospy.init_node('env', anonymous=True)

	world_pub = rospy.Publisher(env_name + '/world_properties', String, queue_size=3)
	sub_name = env_name + '/robot/0/r/twist'
	sub_name = sub_name.replace('/env', '')
	rospy.Subscriber(sub_name, Twist, ball_callback)

	rate = rospy.Rate(50)  # 50hz - 50 times per second

	return world_pub, rate


def publish_world(publisher, body, shape):
	world_list = []

	ball_dir = {'x': body.position.x, 'y': body.position.y, 'r': shape.radius, 'id': 1, 'a': body.angle}

	world_list.append(ball_dir)

	world_dir = {'properties': world_list}
	world_json = json.dumps(world_dir)
	publisher.publish(world_json)


def pymunk_run(world_pub, rate):
	space = pymunk.Space()
	space.gravity = (0, 0)

	space.add(body, shape)

	while not rospy.is_shutdown():
		publish_world(publisher=world_pub, body=body, shape=shape)

		rospy.loginfo(body.position.x)

		space.step(1 / 50.0)
		rate.sleep()


if __name__ == '__main__':
	try:
		world_pub, rate = init_ros(sys.argv[1])
		pymunk_run(world_pub, rate)
	except rospy.ROSInterruptException:
		pass

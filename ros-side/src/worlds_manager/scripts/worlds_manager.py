#!/usr/bin/env python2
# _*_ coding: utf-8 _*_

import rospy
from std_msgs.msg import String
import json

from rospy_message_converter import message_converter

from world.config import config
from world.world import World


worlds = {}
world_create_reqs = []
world_destroy_ids = []


def create_world(world_req):
	world_data = json.loads(world_req.data)

	if world_data['id'] in worlds:
		return
	rospy.loginfo('Creating world: {}'.format(world_data['id']))

	worlds[world_data['id']] = World(world_id=world_data['id'], properties=world_data['world'])


def destroy_world(world_id):
	if world_id.data not in worlds:
		return
	rospy.loginfo('Destroying world: {}'.format(world_id.data))

	worlds[world_id.data].destroy()
	del worlds[world_id.data]


def create_id_append(world_req):
	world_create_reqs.append(world_req)


def destroy_id_append(world_id):
	world_destroy_ids.append(world_id)


def init():
	# creating a ros node
	rospy.init_node(config['manager_config']['name'], anonymous=True)

	# subscribing to create_world and destroy_world topics
	rospy.Subscriber(config['manager_config']['subscribes']['create_world'], String, create_id_append)
	rospy.Subscriber(config['manager_config']['subscribes']['destroy_world'], String, destroy_id_append)


def run():
	init()

	rate = rospy.Rate(config['manager_config']['rate'])

	while not rospy.is_shutdown():
		# creating requested worlds
		for world_req in world_create_reqs:
			create_world(world_req)

		# destroying requested worlds
		for world_id in world_destroy_ids:
			destroy_world(world_id)

		# deleting the lists
		del world_create_reqs[:], world_destroy_ids[:]

		rate.sleep()


if __name__ == '__main__':
	run()

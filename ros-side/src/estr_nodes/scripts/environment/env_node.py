# _*_ coding: utf-8 _*_

import json

import rospy
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Twist
from std_msgs.msg import String

from ros_node import ROSNode
from robot import Robot
from wall import Wall
from config import config

import pymunk


class EnvNode(ROSNode):
	def __init__(self, name):
		ROSNode.__init__(self, config['environment']['name'])

		self.env_name = name
		self.prop_name = self.env_name + '/properties'

		self.__init_properties()

		self.rate = rospy.Rate(config['environment']['rate'])
		self.dt = 1. / config['environment']['rate']

		self.space = pymunk.Space()
		self.space.gravity = (
			self.properties['space_option']['gravity']['x'],
			self.properties['space_option']['gravity']['y'])

		self.robot_pubs = []
		self.robots = []
		self.__init_robots()

		self.walls = []
		self.__init_walls()

		self.__init_env_pub()

	def __init_properties(self):
		self.properties = rospy.get_param(self.prop_name)
		try:
			rospy.delete_param(self.prop_name)
		except KeyError:
			rospy.loginfo('value not set {}'.format(self.prop_name))

	def add_to_pub(self, robot):
		pub_name = self.env_name.replace('env', '')
		pub_name += 'robot/{}/r{}/position'.format(robot.id, robot.script_id)
		self.robot_pubs.append(rospy.Publisher(pub_name, Pose2D, queue_size=config['robots']['pub_que_size']))

	def add_to_sub(self, robot):
		sub_name = self.env_name.replace('env', '')
		sub_name += 'robot/{}/r{}/velocity'.format(robot.id, robot.script_id)
		rospy.Subscriber(sub_name, Twist, robot.update_velocity)

	def __init_robots(self):
		for i in range(len(self.properties['objects']['robots'])):
			robot = Robot(i, self.properties['objects']['robots'][i])
			self.space.add(robot.body, robot.shape)
			self.add_to_pub(robot)
			self.add_to_sub(robot)
			self.robots.append(robot)

	def __init_walls(self):
		for i in range(len(self.properties['objects']['walls'])):
			wall = Wall(i, self.properties['objects']['walls'][i])
			self.space.add(wall.body, wall.shape)
			self.walls.append(wall)

	def __init_env_pub(self):
		pub_name = self.env_name + '/world_properties'
		self.prop_pub = rospy.Publisher(pub_name, String, queue_size=config['environment']['pub_que_size'])

	def publish_robots(self):
		for i in range(len(self.robots)):
			robot = self.robots[i]
			pose = Pose2D()
			pose.x = robot.body.position.x
			pose.y = robot.body.position.y
			pose.theta = robot.body.angle
			self.robot_pubs[i].publish(pose)

	def publish_world_prop(self):
		for i in range(len(self.robots)):
			robot = self.robots[i]
			self.properties['objects']['robots'][i]['x'] = robot.body.position.x
			self.properties['objects']['robots'][i]['y'] = robot.body.position.y
			self.properties['objects']['robots'][i]['r'] = robot.radius
			self.properties['objects']['robots'][i]['a'] = robot.body.angle

		for i in range(len(self.walls)):
			wall = self.walls[i]
			self.properties['objects']['walls'][i]['x'] = wall.body.position.x
			self.properties['objects']['walls'][i]['y'] = wall.body.position.y
			self.properties['objects']['walls'][i]['w'] = wall.width
			self.properties['objects']['walls'][i]['h'] = wall.height
			self.properties['objects']['walls'][i]['a'] = wall.body.angle

		world_dir = {'world': self.properties}
		world_json = json.dumps(world_dir)
		self.prop_pub.publish(world_json)

	def tick(self):
		self.publish_robots()
		self.publish_world_prop()

		self.space.step(self.dt)

		self.rate.sleep()

	def run(self):
		while not rospy.is_shutdown():
			self.tick()

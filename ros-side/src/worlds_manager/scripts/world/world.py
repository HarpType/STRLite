# _*_ coding: utf-8 _*_

from roslaunch.scriptapi import ROSLaunch

from nodes.environment import EnvNode
from namespace import Namespace
from .robot import Robot


class World:
	def __init__(self, world_id, properties):
		self.name = Namespace(namespace='world/', name=world_id)
		self.properties = properties

		self.__init_launch()

		self.env = EnvNode(owner=self, properties=self.properties)
		self.env.launch(self.launch.launch)

		self.robots = []
		self.__init_robots()
		self.launch_robots()

	def __init_launch(self):
		self.launch = ROSLaunch()
		self.launch.start()

	def __init_robots(self):
		for i in range(len(self.properties['objects']['robots'])):
			robot = Robot(owner=self, robot_id=str(i))
			self.robots.append(robot)

	def launch_robots(self):
		for i in range(len(self.properties['objects']['robots'])):
			self.robots[i].launch_RTS(self.launch.launch)

	def destroy(self):
		self.env.stop()

		for i in range(len(self.properties['objects']['robots'])):
			self.robots[i].stop_RTS()

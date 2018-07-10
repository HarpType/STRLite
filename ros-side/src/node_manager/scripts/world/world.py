from roslaunch.scriptapi import ROSLaunch

from environment import Environment
from namespace import Namespace


class World:

	def __init__(self, world_id, world_init_prop):
		self.name = Namespace(namespace='/world/', name=world_id)
		self.__init_properties = world_init_prop

		self.launch = None
		self.__init_launch()

		self.__env = Environment(owner=self, properties=self.__init_properties)

	def __init_launch(self):
		self.launch = ROSLaunch()
		self.launch.start()

	def destroy(self):
		pass

# _*_ coding: utf-8 _*_

from namespace import Namespace
from runners.r_node_runner import RNodeRunner


class Robot:
	def __init__(self, owner, robot_id, properties):
		self.name = Namespace(namespace=owner.name.create_namespace()+'robot/', name=robot_id)
		self.properties = properties

		self.__init_RTS()

	def __init_RTS(self):
		self._r_node_runner = RNodeRunner(self, self.properties['script_id'])

	def launch_RTS(self, launch):
		self._r_node_runner.launch(launch)

	def stop_RTS(self):
		self._r_node_runner.stop()

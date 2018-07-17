# _*_ coding: utf-8 _*_

from namespace import Namespace
from runners.r_node_runner import RNodeRunner


class Robot:
	def __init__(self, owner, robot_id):
		self.name = Namespace(namespace=owner.name.create_namespace()+'robot/', name=robot_id)

		self.__init_RTS()

	def __init_RTS(self):
		self._r_node_runner = RNodeRunner(self)

	def launch_RTS(self, launch):
		self._r_node_runner.launch(launch)

	def stop_RTS(self):
		self._r_node_runner.stop()

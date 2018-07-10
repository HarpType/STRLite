from roslaunch.core import Node
import rospy

from namespace import Namespace
from config import config


class Environment:

	def __init__(self, owner, properties):
		self.__owner = owner
		self.name = Namespace(namespace=self.__owner.name.create_namespace(), name='env')
		self.__init_properties = properties

		self.__pkg_name = config['launch_paths']['env']['package']
		self.__executable = config['launch_paths']['env']['executable']

		self.__proc_env = None

	def launch(self):
		"""
		This method sets up information about the env node and runs it
		"""
		node = Node(package=self.__pkg_name, node_type=self.__executable, args=self.name.get_full_name())
		self.__proc_env = self.__owner.launch.launch(node)
		rospy.loginfo("Launching env node: {}".format(self.name.get_full_name()))

	def stop(self):
		self.__proc_env.stop()

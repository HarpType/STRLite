# _*_ coding: utf-8 _*_

import rospy

from rospy_message_converter import message_converter

from .node_manager import NodeManager
from ..config import config


class EnvNode(NodeManager):
	def __init__(self, owner, properties):
		NodeManager.__init__(
			self, namespace=owner.name.create_namespace(), name='env',
			pkg_name=config['launch_paths']['env']['package'],
			exec_name=config['launch_paths']['env']['executable'])

		self._owner = owner
		self.properties = properties

	def launch(self, launch):
		# world_msg = message_converter.convert_dictionary_to_ros_message(self.properties)
		# rospy.set_param(self.name.get_full_name()+'world', world_msg)
		NodeManager.launch(self, launch)

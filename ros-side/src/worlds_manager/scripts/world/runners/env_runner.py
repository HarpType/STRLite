# _*_ coding: utf-8 _*_

import json

import rospy

from .runner import Runner
from ..config import config


class EnvNode(Runner):
	def __init__(self, owner, properties):
		Runner.__init__(
			self, namespace=owner.name.create_namespace(), name='env',
			pkg_name=config['launch_paths']['env']['package'],
			exec_name=config['launch_paths']['env']['executable'])

		self._owner = owner
		self.properties = properties

	def launch(self, launch):
		rospy.set_param(self.name.create_namespace()+'properties', self.properties)
		Runner.launch(self, launch)

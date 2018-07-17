# _*_ coding: utf-8 _*_

from runner import Runner
from ..config import config


class RNodeRunner(Runner):
	def __init__(self, owner):
		Runner.__init__(
			self, namespace=owner.name.create_namespace(), name='r',
			pkg_name=config['launch_paths']['RTS']['package'],
			exec_name=config['launch_paths']['RTS']['r'])

# _*_ coding: utf-8 _*_

from runner import Runner
from ..config import config


class RNodeRunner(Runner):
	def __init__(self, owner, script_id):
		Runner.__init__(
			self, namespace=owner.name.create_namespace(), name='r'+str(script_id),
			pkg_name=config['launch_paths']['RTS']['package'],
			exec_name='r'+str(script_id)+'.py')

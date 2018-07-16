# _*_ coding: utf-8 _*_

from node_manager import NodeManager
from ..config import config


class RNode(NodeManager):
	def __init__(self, owner):
		NodeManager.__init__(
			self, namespace=owner.name.create_namespace(), name='r',
			pkg_name=config['launch_paths']['RTS']['package'],
			exec_name=config['launch_paths']['RTS']['r'])

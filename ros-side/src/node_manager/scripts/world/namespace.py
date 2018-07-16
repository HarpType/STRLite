# _*_ coding: utf-8 _*_

"""
	This class provides namespaces. Namespaces are used to set up unique ROS nodes.
"""


class Namespace:

	def __init__(self, namespace='', name='untitled'):
		self._namespace = namespace
		self._name = name

	def get_namespace(self):
		return self._namespace

	def get_name(self):
		return self._name

	def get_full_name(self):
		return self._namespace + self._name

	def create_namespace(self):
		return self._namespace + self._name + '/'

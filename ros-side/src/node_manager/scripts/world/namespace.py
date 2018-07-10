"""
	This class provides namespaces. Namespaces are used to set up unique ROS nodes.
"""


class Namespace:

	def __init__(self, namespace='', name='untitled'):
		self.__namespace = namespace
		self.__name = name

	def get_namespace(self):
		return self.__namespace

	def get_name(self):
		return self.__name

	def get_full_name(self):
		return self.__namespace + self.__name

	def create_namespace(self):
		return self.__namespace + self.__name + '/'

# _*_ coding: utf-8 _*_

from roslaunch.core import Node
import rospy

from ..namespace import Namespace


class NodeManager:
	def __init__(self, namespace, name, pkg_name, exec_name):
		self.name = Namespace(namespace=namespace, name=name)
		self._pkg_name = pkg_name
		self._executable = exec_name

		self._proc_env = None

	def launch(self, launch):
		node = Node(package=self._pkg_name, node_type=self._executable, args=self.name.get_full_name())
		self._proc_env = launch(node)
		rospy.loginfo("Launching node: {}".format(self.name.get_full_name()))

	def stop(self):
		self._proc_env.stop()

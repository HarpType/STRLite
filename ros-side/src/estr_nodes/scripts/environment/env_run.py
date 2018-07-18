#!/usr/bin/env python2
# _*_ coding: utf-8 _*_

import sys

import rospy

from env_node import EnvNode

if __name__ == "__main__":
	try:
		env = EnvNode(sys.argv[1])
		env.run()
	except rospy.ROSInterruptException:
		pass

import rospy


class ROSNode:
	def __init__(self, node_name):
		rospy.init_node(node_name, anonymous=True)

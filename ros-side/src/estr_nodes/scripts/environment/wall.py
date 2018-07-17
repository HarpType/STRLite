import pymunk
import rospy


class Wall:
	def __init__(self, wall_id, properties):
		self.id = wall_id
		self.__init_basis(properties)

	def __init_basis(self, properties):
		self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
		self.body.position = (properties['x'], properties['y'])
		self.body.angle = properties['a']
		self.width = properties['w']
		self.height = properties['h']
		if self.width < self.height:
			h_half = self.height / 2.
			point1 = (0, -h_half)
			point2 = (0, h_half)
			self.shape = pymunk.Segment(self.body, point1, point2, self.width / 2.)
		else:
			w_half = self.width / 2.0
			point1 = (- w_half, 0)
			point2 = (w_half, 0)
			self.shape = pymunk.Segment(self.body, point1, point2, self.height / 2.)

		self.shape.friction = 0.5 # hardcoding!!!

"""	def __init_basis(self, properties):
		self.width = properties['w']
		self.height = properties['h']
		w_half = self.width
		point1 = (properties['x'] - w_half, properties['y'])
		point2 = (properties['x'] + w_half, properties['y'])
		self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
		self.body.position = (properties['x'], properties['y'])
		self.body.angle = properties['a']
		self.shape = pymunk.Segment(self.body, point1, point2, self.height)
"""
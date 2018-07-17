import pymunk


class Wall:
	def __init__(self, wall_id, properties):
		self.id = wall_id

		self.__init_basis(properties)

	def __init_basis(self, properties):
		self.weight = properties['w']
		self.height = properties['h']
		w_half = self.weight / 2.0
		point1 = (properties['x'] - w_half, properties['y'])
		point2 = (properties['x'] + w_half, properties['y'])
		self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
		self.body.position = (properties['x'], properties['y'])
		self.body.angle = properties['a']
		self.shape = pymunk.Segment(self.body, point1, point2, self.height)

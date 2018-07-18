import pymunk

from config import config


class Robot:
	def __init__(self, robot_id, properties, gravity_type):
		self.id = robot_id
		self.script_id = properties['script_id']

		self.__init_basis(properties)

		self.gravity_type = gravity_type

	def __init_body(self):
		self.mass = config['robots']['mass']
		self.moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
		self.body = pymunk.Body(self.mass, self.moment)

	def __init_basis(self, properties):
		self.radius = properties['r']
		self.__init_body()
		self.body.position = (properties['x'], properties['y'])
		self.body.angle = properties['a']
		self.shape = pymunk.Circle(self.body, self.radius, (0, 0))
		self.shape.friction = config['robots']['friction']

	def update_velocity(self, msg):
		# hardcoding!!! TODO: wrappers
		# self.body._set_velocity((msg.linear.x, self.body.velocity.y+msg.linear.y))
		# self.body.apply_impulse_at_local_point((self.mass*msg.linear.x, self.mass*msg.linear.y))
		if self.gravity_type == 0:
			self.body._set_velocity((msg.linear.x, self.body.velocity.y))
		else:
			self.body._set_velocity((msg.linear.x, msg.linear.y))

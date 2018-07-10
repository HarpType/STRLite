import sys
import time
import random
import pymunk
import pickle


def add_ball(space):
	mass = 1
	radius = 14

	moment = pymunk.moment_for_circle(mass, 0, radius)
	body = pymunk.Body(mass, moment)

	x = random.randint(160, 380)
	body.position = (x, 550)
	shape = pymunk.Circle(body, radius)

	space.add(body, shape)

	return shape

def add_static_l(space):
	body = pymunk.Body(body_type=pymunk.Body.STATIC)
	body.position = (300, 300)

	l1 = pymunk.Segment(body, (-150, 0), (150, 0), 5)
	l2 = pymunk.Segment(body, (-150, 0), (-150, 50), 5)
	l3 = pymunk.Segment(body, (150, 0), (150, 50), 5)
	
	d_l1 = {'x': l1.body.position.x, 'y': l1.body.position.y, 'id': 2, 'w': 300, 'h': 5, 'a': 0}
	d_l2 = {'x': l2.body.position.x-150, 'y': l2.body.position.y, 'id': 2, 'w': 5, 'h': 50, 'a': 0}
	d_l3 = {'x': l3.body.position.x+150, 'y': l3.body.position.y, 'id': 2, 'w': 5, 'h': 50, 'a': 0}
	
	space.add(l1, l2, l3)

	return [d_l1, d_l2, d_l3]

def stdout_balls(balls, statics):
	balls_list = list()

	for ball in balls:
		ball_dir = {'x': ball.body.position.x, 'y': ball.body.position.y, 'r': ball.radius, 'id': 1, 'a': 45}
		balls_list.append(ball_dir)

	#print("gravity: ", balls_list)
	balls_list.extend(statics)

	sys.stdout.write('COMMAND' + str(balls_list) + '\n')


if __name__ == '__main__':
	space = pymunk.Space()
	space.gravity = (0, -900)
	dt = 1 / 50

	statics_l = add_static_l(space)

	balls = list()
	ticks_to_next_ball = 10

	sys.stdout.write("COMMANDReady\n")

	while True:

		ticks_to_next_ball -= 1
		if ticks_to_next_ball <= 0:
			ticks_to_next_ball = 25
			ball_shape = add_ball(space)
			balls.append(ball_shape)

		balls_to_remove = []
		for ball in balls:
			if ball.body.position.y < 0:
				balls_to_remove.append(ball)

		for ball in balls_to_remove:
			space.remove(ball, ball.body)
			balls.remove(ball)

		space.step(dt)

		stdout_balls(balls, statics_l)

		time.sleep(dt)

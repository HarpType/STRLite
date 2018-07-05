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


def stdout_balls(balls):
	balls_list = list()

	for ball in balls:
		ball_dir = {'x': ball.body.position.x, 'y': ball.body.position.y, 'r': ball.radius}
		balls_list.append(ball_dir)

	#print("gravity: ", balls_list)

	sys.stdout.write('COMMAND' + str(balls_list) + '\n')


if __name__ == '__main__':
	space = pymunk.Space()
	space.gravity = (0, -900)
	dt = 1 / 50

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

		stdout_balls(balls)

		time.sleep(dt)

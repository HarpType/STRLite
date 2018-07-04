import os
from pathlib import Path
import mmap
import pickle
import time

import random

import pymunk

rel_path = 'web-side/strl/strl_app/relation'
cur_path = os.getcwd()
# to STRLite
par_path = Path(cur_path).parent
# the path where .dat files exist
files_path = par_path.joinpath(*rel_path.split('/'))

f1 = open(str(files_path.joinpath('c_to_p.dat')), 'r+')
f2 = open(str(files_path.joinpath('p_to_c.dat')), 'r+')
size = 1024

data1 = mmap.mmap(f1.fileno(), size)
data2 = mmap.mmap(f2.fileno(), size)


def add_ball(space):
	mass = 1
	radius = 14

	moment = pymunk.moment_for_circle(mass, 0, radius)
	body = pymunk.Body(mass, moment)

	x = random.randint(150, 380)
	shape = pymunk.Circle(body, radius)

	space.add(body, shape)

	return shape


def send_balls(balls):
	balls_list = list()
	for ball in balls:
		ball_dir = {'x': ball.body.position.x(), 'y': ball.body.position.y(), 'r': ball.radius}
		print(ball_dir)
		balls_list.append(ball_dir)

	pickle.dump(balls_list, data1)


if __name__ == '__main__':
	space = pymunk.Space()
	space.gravity = (0, -900)
	dt = 1 / 50

	balls = list()
	ticks_to_next_ball = 10

	data1[0] = "R"

	while True:
		if data2[0] == 'S':
			break

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

		send_balls(balls)

		time.sleep(dt)

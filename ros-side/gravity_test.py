import sys
import time

import random
import pygame
from pygame.locals import *
import pymunk
from pymunk import pygame_util


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


def send_balls(balls):
	balls_list = list()
	for ball in balls:
		ball_dir = {'x': 600-ball.body.position.x, 'y': 600-ball.body.position.y, 'r': ball.radius}
		balls_list.append(ball_dir)

	print(balls_list)


if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((600, 600))
	pygame.display.set_caption("Joints. Just wait and the L will tip over")
	clock = pygame.time.Clock()

	space = pymunk.Space()
	space.gravity = (0, -900)
	dt = 1 / 50

	balls = list()
	draw_options = pygame_util.DrawOptions(screen)
	ticks_to_next_ball = 10

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				sys.exit(0)

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

		screen.fill((255, 255, 255))
		space.debug_draw(draw_options)

		pygame.display.flip()
		clock.tick(50)

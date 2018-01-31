# Python3/tkinter implementation of classic arcade game Pong

import tkinter
from tkinter import *
import random
import math

# globals
REFRESH_RATE = 60
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
PAD_VEL = 4
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True


# class implementing pong game using Tkinter GUI library
class pong(object):

    #class variables
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [5, 5]
    left_paddle_pos = HEIGHT / 2
    right_paddle_pos = HEIGHT / 2
    left_paddle_vel = 0
    right_paddle_vel = 0
    left_score = 0
    right_score = 0

    def __init__(self):
        # create Canvas
        self.root = Tk()
        self.canvas = Canvas(
            self.root, width=WIDTH, height=HEIGHT, background="Black")
        self.canvas.pack()
        # draw mid line and gutters
        self.middle_line = self.canvas.create_line(
            WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill="Gray")
        self.left_goal_line = self.canvas.create_line(
            PAD_WIDTH, 0, PAD_WIDTH, HEIGHT, fill="Gray")
        self.right_goal_line = self.canvas.create_line(
            WIDTH - PAD_WIDTH, 0, WIDTH - PAD_WIDTH, HEIGHT, fill="Gray")
        # draw ball
        self.ball = self.canvas.create_oval(
            self.ball_pos[0] - BALL_RADIUS,
            self.ball_pos[1] - BALL_RADIUS,
            self.ball_pos[0] + BALL_RADIUS,
            self.ball_pos[1] + BALL_RADIUS,
            fill="White")
        # draw paddles
        self.left_pad = self.canvas.create_line(
            HALF_PAD_WIDTH,
            self.left_paddle_pos - HALF_PAD_HEIGHT,
            HALF_PAD_WIDTH,
            self.left_paddle_pos + HALF_PAD_HEIGHT,
            fill="White",
            width=PAD_WIDTH)
        self.right_pad = self.canvas.create_line(
            WIDTH - HALF_PAD_WIDTH,
            self.right_paddle_pos - HALF_PAD_HEIGHT,
            WIDTH - HALF_PAD_WIDTH,
            self.right_paddle_pos + HALF_PAD_HEIGHT,
            fill="White",
            width=PAD_WIDTH)
        # bind handlers and start mainloop and updating canvas
        self.root.bind("<KeyPress>", self.keyPress)
        self.root.bind("<KeyRelease>", self.keyRelease)
        self.new_game
        self.root.after(int((1 / REFRESH_RATE) * 1000), self.draw)
        self.root.mainloop()

    # create new game
    def new_game():
        self.left_score = 0
        self.right_score = 0
        spawn_ball(RIGHT)

    # spawn new ball either left or right
    def spawn_ball(self, direction):
        self.ball_pos[0] = WIDTH / 2
        self.ball_pos[1] = HEIGHT / 2
        self.ball_vel[0] = random.randrange(3, 6)
        self.ball_vel[1] = -(random.randrange(1, 3))
        if direction == LEFT:
            self.ball_vel[0] = -(self.ball_vel[0])
        self.canvas.delete(self.ball)
        self.ball = self.canvas.create_oval(
            self.ball_pos[0] - BALL_RADIUS,
            self.ball_pos[1] - BALL_RADIUS,
            self.ball_pos[0] + BALL_RADIUS,
            self.ball_pos[1] + BALL_RADIUS,
            fill="White")

    # keypress event
    def keyPress(self, event):
        if event.keysym == "Up":
            self.right_paddle_vel = -PAD_VEL
        elif event.keysym == "Down":
            self.right_paddle_vel = PAD_VEL
        elif event.keysym == "w":
            self.left_paddle_vel = -PAD_VEL
        elif event.keysym == "s":
            self.left_paddle_vel = PAD_VEL

    # keyrelease event
    def keyRelease(self, event):
        if event.keysym == "Up":
            self.right_paddle_vel = 0
        elif event.keysym == "Down":
            self.right_paddle_vel = 0
        elif event.keysym == "w":
            self.left_paddle_vel = 0
        elif event.keysym == "s":
            self.left_paddle_vel = 0

    def draw(self):
        # calculate ball X-axis position
        if (self.ball_pos[0] - BALL_RADIUS) < PAD_WIDTH:
            if abs(self.left_paddle_pos - self.ball_pos[1]) < HALF_PAD_HEIGHT:
                self.ball_vel[0] = -(self.ball_vel[0] * 1.1)
                self.ball_vel[1] = self.ball_vel[1] * 1.1
            else:
                self.spawn_ball(RIGHT)
                self.right_score += 1
        elif (self.ball_pos[0] + BALL_RADIUS) > (WIDTH - PAD_WIDTH):
            if abs(self.right_paddle_pos - self.ball_pos[1]) < HALF_PAD_HEIGHT:
                self.ball_vel[0] = -(self.ball_vel[0] * 1.1)
                self.ball_vel[1] = self.ball_vel[1] * 1.1
            else:
                self.spawn_ball(LEFT)
                self.left_score += 1
        # calculate ball Y-axis position
        if self.ball_pos[1] < BALL_RADIUS:
            self.ball_vel[1] = -(self.ball_vel[1])
        elif (self.ball_pos[1] + BALL_RADIUS) > HEIGHT:
            self.ball_vel[1] = -(self.ball_vel[1])
        # update ball position
        self.ball_pos[0] += self.ball_vel[0]
        self.ball_pos[1] += self.ball_vel[1]
        self.canvas.move(self.ball, self.ball_vel[0], self.ball_vel[1])
        # update left paddle
        if self.left_paddle_vel < 0:
            if self.left_paddle_pos > HALF_PAD_HEIGHT:
                self.left_paddle_pos += self.left_paddle_vel
                self.canvas.move(self.left_pad, 0, self.left_paddle_vel)
        if self.left_paddle_vel > 0:
            if self.left_paddle_pos + HALF_PAD_HEIGHT < HEIGHT:
                self.left_paddle_pos += self.left_paddle_vel
                self.canvas.move(self.left_pad, 0, self.left_paddle_vel)
        # update right paddle
        if self.right_paddle_vel < 0:
            if self.right_paddle_pos > HALF_PAD_HEIGHT:
                self.right_paddle_pos += self.right_paddle_vel
                self.canvas.move(self.right_pad, 0, self.right_paddle_vel)
        if self.right_paddle_vel > 0:
            if self.right_paddle_pos + HALF_PAD_HEIGHT < HEIGHT:
                self.right_paddle_pos += self.right_paddle_vel
                self.canvas.move(self.right_pad, 0, self.right_paddle_vel)
        # call next refresh
        self.root.after(int((1 / REFRESH_RATE) * 1000), self.draw)


# start pong
pong()

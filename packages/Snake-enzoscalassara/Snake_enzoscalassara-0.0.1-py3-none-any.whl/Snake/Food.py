from turtle import Turtle
from random import randrange


class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.food_list = []
        self.shape("circle")
        self.color("blue")
        self.turtlesize(stretch_len=0.5, stretch_wid=0.5)
        self.penup()
        self.speed(10)

#   When food is eaten, this method will move it to a new location.
    def refresh(self):
        cord_x = randrange(-280, 280, 10)
        cord_y = randrange(-280, 280, 10)
        self.goto(cord_x, cord_y)

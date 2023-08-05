from turtle import Turtle


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.goto(0, 270)
        self.hideturtle()
        self.point_counter = 0
        self.color("White")

    def point(self):
        self.write(f"Score: {self.point_counter}", align='center', font=('Arial', 18, 'normal'))
        self.point_counter += 1

from turtle import Turtle


class Snake:

    def __init__(self):
        self.snake_body = []
        self.snake_starting_size = 3
        self.snake_speed = 10

#       Made a new turtle to set the snake head apart from its body, without removing it from the list.
        new_snake_square = Turtle()
        new_snake_square.shape("square")
        new_snake_square.color("white")
        new_snake_square.penup()
        new_snake_square.goto((-20), 0)
        new_snake_square.speed(1)
        self.snake_body.append(new_snake_square)
        self.snake_head = self.snake_body[0]

    def create_snake(self):
        i = 1
        for _ in range(self.snake_starting_size - 1):
            new_snake_square = Turtle()
            new_snake_square.shape("square")
            new_snake_square.color("white")
            new_snake_square.penup()
            new_snake_square.goto((i * -20), 0)
            new_snake_square.speed(1)
            self.snake_body.append(new_snake_square)
            i += 1

#   This method increases the snake size, meant to be called when food is eaten.
    def eat_food(self):
        j = len(self.snake_body)
        new_snake_square = Turtle()
        new_snake_square.shape("square")
        new_snake_square.color("white")
        new_snake_square.penup()
        new_snake_square.speed(1)
        new_snake_square.setheading(self.snake_body[j-1].heading())

#       These conditionals are used to tell where the new extension of the snake's body should appear.
        if new_snake_square.heading() == 0:
            new_snake_square.goto((self.snake_body[j - 1].xcor() - 20), self.snake_body[j - 1].ycor())

        elif new_snake_square.heading() == 90:
            new_snake_square.goto((self.snake_body[j - 1].xcor()), (self.snake_body[j - 1].ycor() + 20))

        elif new_snake_square.heading() == 180:
            new_snake_square.goto((self.snake_body[j - 1].xcor() + 20), self.snake_body[j - 1].ycor())

        elif new_snake_square.heading() == 270:
            new_snake_square.goto((self.snake_body[j - 1].xcor()), (self.snake_body[j - 1].ycor() - 20))

        self.snake_body.append(new_snake_square)

    def face_east(self):
        if self.snake_body[0].heading() != 0 and self.snake_body[0].heading() != 180:
            self.snake_body[0].setheading(0)

    def face_north(self):
        if self.snake_body[0].heading() != 90 and self.snake_body[0].heading() != 270:
            self.snake_body[0].setheading(90)

    def face_west(self):
        if self.snake_body[0].heading() != 180 and self.snake_body[0].heading() != 0:
            self.snake_body[0].setheading(180)

    def face_south(self):
        if self.snake_body[0].heading() != 270 and self.snake_body[0].heading() != 90:
            self.snake_body[0].setheading(270)

#   Makes the body of the snake follow its head.
    def trace_and_movement(self):
        i = len(self.snake_body) - 1
        for _ in range(len(self.snake_body) - 1):
            self.snake_body[i].goto(self.snake_body[i - 1].xcor(), (self.snake_body[i - 1].ycor()))
            i -= 1
        self.snake_head.forward(self.snake_speed)

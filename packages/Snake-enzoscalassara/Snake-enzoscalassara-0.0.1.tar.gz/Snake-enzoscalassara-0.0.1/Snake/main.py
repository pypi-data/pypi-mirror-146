from Food import Food
from turtle import Screen, Turtle
from snake import Snake
from scoreboard import Scoreboard
import time

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake game")
screen.tracer(0)

snake = Snake()
snake.snake_starting_size = 5
snake.snake_speed = 10


snake.create_snake()


food = Food()
food.refresh()


scoreboard = Scoreboard()
scoreboard.point()


game_over = False


# Inputs
screen.listen()
screen.onkey(key="d", fun=snake.face_east)
screen.onkey(key="w", fun=snake.face_north)
screen.onkey(key="a", fun=snake.face_west)
screen.onkey(key="s", fun=snake.face_south)


while not game_over:
    screen.update()
    time.sleep(0.1)

#   Detects collision with food.
    if snake.snake_head.distance(food) < 15:
        food.refresh()
        snake.eat_food()
        scoreboard.clear()
        scoreboard.point()
    snake.trace_and_movement()

#   Detects collision with wall.
    if snake.snake_head.xcor() > 280 or snake.snake_head.xcor() < -280 or snake.snake_head.ycor() > 280 or \
            snake.snake_head.ycor() < -280:
        game_over = True

#   Detects collision with body.
    for squares in snake.snake_body[2:]:
        if snake.snake_head.distance(squares) < 10:
            game_over = True

#   Game over text on screen.
    if game_over:
        game_over_text = Turtle()
        game_over_text.penup()
        game_over_text.hideturtle()
        game_over_text.color("Red")
        game_over_text.write('GAME OVER', align='center', font=('Arial', 18, 'normal'))


screen.exitonclick()

from turtle import Screen, Turtle
import time


class Bricks(Turtle):    # A class to create all bricks and save them on a list

    def __init__(self):
        super().__init__()
        self.all_bricks = []

    def bricks_build_up(self):
        for y in range(30, 370, 30):
            x = -360
            for n in range(0, 14):
                new_brick = Turtle("square")
                new_brick.color("yellow")
                new_brick.shapesize(stretch_wid=1, stretch_len=2.5)
                new_brick.penup()
                position = (x, y)
                new_brick.goto(position)
                if 30 <= y <= 120:
                    new_brick.color("red")
                if 121 <= y <= 240:
                    new_brick.color("blue")
                x += 55
                self.all_bricks.append(new_brick)


class Paddle(Turtle):     # A class to create the paddle and its movement

    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=0.5, stretch_len=6)
        self.penup()
        self.speed(0)
        self.goto(0, -400)

    def move_left(self):
        new_x = self.xcor() - 20
        if new_x >= - 340:
            self.goto(new_x, self.ycor())
        else:
            pass

    def move_right(self):
        new_x = self.xcor() + 20
        if new_x <= 330:
            self.goto(new_x, self.ycor())
        else:
            pass


class Ball(Turtle):          # A class to create them ball and its movement

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.shapesize(0.5)
        self.color("white")
        self.penup()
        self.goto(0, 0)
        self.speed(1)
        self.x_move = -5
        self.y_move = -10
        self.move_speed = 0.08

    def ball_movement(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1

    def reset_position(self):
        self.move_speed = 0.1
        self.goto(0, 0)
        self.bounce_x()


class Score(Turtle):               # A class to create the score, show it and update it

    def __init__(self):
        super().__init__()

        self.color("white")
        self.penup()
        self.hideturtle()
        self.score = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(-300, 400)
        self.write(f"Score:{self.score}", align="center", font=("Courier", 20, "normal"))

    def point(self):
        self.score += 100
        self.update_scoreboard()


class Lives(Turtle):          # A similar to score class but for player's lives

    def __init__(self):
        super().__init__()

        self.color("white")
        self.penup()
        self.hideturtle()
        self.lives = 5
        self.update_lives_board()

    def update_lives_board(self):
        self.clear()
        self.goto(300, 400)
        self.write(f"Lives:{self.lives}", align="center", font=("Courier", 20, "normal"))

    def lose_life(self):
        self.lives -= 1
        self.update_lives_board()


def border_creation():           # A function that creates the boarders
    border_corners = {"top_left": (-395, 390), "bottom_left": (-395, -440),
                      "bottom_right": (390, -440), "top_right": (390, 390)}
    border = Turtle()
    border.speed(0)
    border.hideturtle()
    border.penup()
    border.color("white")
    border.width(10)
    border.goto(390, 390)
    border.pendown()
    for corner in border_corners:
        border.goto(border_corners[corner])


def game_over(user_lives):           # A function that shows a message when game is over either player is out of lives
    global game_is_on                # or all bricks are broken
    game_over_sign = Turtle()
    game_over_sign.hideturtle()
    game_over_sign.penup()
    game_over_sign.color("white")
    game_over_sign.width(20)
    game_over_sign.goto(0, 0)
    if user_lives == 0:
        game_over_sign.write(f"GAME OVER", align="center", font=("Courier", 50, "normal"))
    else:
        game_over_sign.write("CONGRATULATIONS", align="center", font=("Courier", 30, "normal"))
        game_over_sign.goto(0, -50)
        game_over_sign.write(f"YOUR SCORE IS: {score.score}", align="center", font=("Courier", 30, "normal"))


# Initialisation of the game screen and all the objects of the game
game_screen = Screen()
game_screen.setup(width=800, height=900)
game_screen.bgcolor("black")
game_screen.title("Breakout")
game_screen.tracer(0)

border_creation()

paddle = Paddle()

ball = Ball()

score = Score()

lives = Lives()

game_screen.listen()
game_screen.onkey(fun=paddle.move_left, key="Left")
game_screen.onkey(fun=paddle.move_right, key="Right")


bricks = Bricks()
bricks.bricks_build_up()


collisions = 0
game_is_on = True

while game_is_on:          # Main loop of the game, determines ball's movement and if a brick is broken
    time.sleep(ball.move_speed)
    game_screen.update()
    ball.ball_movement()
    ball_position = (ball.xcor(), ball.ycor())
    if ball.xcor() > 375 or ball.xcor() < -380:
        ball.bounce_x()

    if ball.ycor() > 375:
        ball.bounce_y()

    if ball.distance(paddle) < 50 and ball.ycor() < -385:
        ball.bounce_y()

    if ball.ycor() < - 420:
        ball.reset_position()
        lives.lose_life()
        if lives.lives == 0:
            game_is_on = False
            game_over(lives.lives)

    for brk in bricks.all_bricks:
        if ball.distance(brk) <= 30:
            brk.hideturtle()
            bricks.all_bricks.remove(brk)
            score.point()
            if ball.ycor() < brk.ycor():
                ball.bounce_y()
            elif ball.ycor() > brk.ycor():
                ball.bounce_y()
            elif ball.xcor() < brk.xcor():
                ball.bounce_x()
            elif ball.xcor() > brk.xcor():
                ball.bounce_x()
    if len(bricks.all_bricks) == 0:
        game_over(lives.lives)
        game_is_on = False
        game_screen.update()

game_screen.exitonclick()

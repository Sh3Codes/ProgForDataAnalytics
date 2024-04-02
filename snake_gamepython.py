from tkinter import *
import random

# Game constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 200
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#0000FF"  # Changed to blue color
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
GAME_OVER_COLOR = "#FFFF00"  # Yellow color for "Game Over" text
OBSTACLE_COLOR = "#FFFF00"   # Changed to yellow for obstacles

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, obstacles):
        self.coordinates = self.generate_food_location(obstacles)
        canvas.create_oval(self.coordinates[0], self.coordinates[1], self.coordinates[0] + SPACE_SIZE, self.coordinates[1] + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

    def generate_food_location(self, obstacles):
        while True:
            x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
            # Check if the food coordinates overlap with any obstacle
            if not any(x == obstacle.coordinates[0] and y == obstacle.coordinates[1] for obstacle in obstacles):
                return [x, y]

class Obstacle:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=OBSTACLE_COLOR, tag="obstacle")

def next_turn(snake, food, obstacles):
    global direction

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))

        canvas.delete("food")
        food = Food(obstacles)
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake, obstacles):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food, obstacles)

def change_direction(new_direction):
    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake, obstacles):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    
    for obstacle in obstacles:
        if x == obstacle.coordinates[0] and y == obstacle.coordinates[1]:
            return True

    return False

def game_over():
    global score
    global high_score

    if score > high_score:
        high_score = score
        high_score_label.config(text="High Score: {}".format(high_score))
        save_high_score(high_score)

    canvas.delete(ALL)
    canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2,
                       font=('consolas',70), text="GAME OVER", fill=GAME_OVER_COLOR, tag="gameover")
    canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2 + 100,
                       font=('consolas',20), text="Press 'R' to retry", fill="white", tag="retry")
    label.config(text="Score: {}".format(score))
    window.bind('<Key>', restart_game)

def restart_game(event=None):
    global snake
    global food
    global obstacles
    global score

    score = 0
    label.config(text="Score: {}".format(score))
    
    canvas.delete("all")
    snake = Snake()
    food = Food(obstacles)
    obstacles = [Obstacle() for _ in range(5)]  # Add 5 obstacles
    next_turn(snake, food, obstacles)

def save_high_score(score):
    try:
        with open("high_score.txt", "w") as file:
            file.write(str(score))
    except Exception as e:
        print("An error occurred while saving the high score:", e)

def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0
    except Exception as e:
        print("An error occurred while loading the high score:", e)
        return 0

window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'
high_score = load_high_score()

label = Label(window, text="Score: {}".format(score), font=('consolas', 40))
label.pack()

high_score_label = Label(window, text="High Score: {}".format(high_score), font=('consolas', 20))
high_score_label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

exit_button = Button(window, text="Exit", command=window.destroy)
exit_button.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<r>', restart_game)  # Press 'r' to restart the game

snake = Snake()
food = Food([])
obstacles = [Obstacle() for _ in range(5)]  # Add 5 obstacles

next_turn(snake, food, obstacles)

window.mainloop()
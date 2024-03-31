import tkinter as tk
import random

def check_guess():
    global n, attempts_left
    guess = int(guess_entry.get())
    attempts_left -= 1
    if guess < n:
        result_label.config(text="Too low")
    elif guess > n:
        result_label.config(text="Too high!")
    else:
        result_label.config(text="You guessed it right! Congratulations!!")
        guess_entry.config(state='disabled')
        submit_button.config(state='disabled')
    if attempts_left == 0:
        result_label.config(text=f"Sorry, you've used all your attempts. The correct number was {n}")
        guess_entry.config(state='disabled')
        submit_button.config(state='disabled')

n = random.randrange(1, 20)
attempts_left = 5

root = tk.Tk()
root.title("Number Guessing Game")

# Setting background color to red
root.configure(bg='red')

canvas = tk.Canvas(root, width=400, height=300, bg='red')  # Setting canvas background color to blue
canvas.pack()

guess_label = tk.Label(root, text="Enter any number:", bg='yellow')  # Setting label background color to red
guess_label.place(x=50, y=50)

guess_entry = tk.Entry(root)
guess_entry.place(x=200, y=50)

submit_button = tk.Button(root, text="Submit", command=check_guess, bg='yellow')  # Setting button background color to red
submit_button.place(x=150, y=100)

result_label = tk.Label(root, text="", bg='red')  # Setting result label background color to red
result_label.place(x=150, y=150)

root.mainloop()
 
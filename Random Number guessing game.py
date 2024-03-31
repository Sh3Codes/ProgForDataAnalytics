import tkinter as tk
import random

def check_guess():
    global n
    guess = int(guess_entry.get())
    if guess < n:
        result_label.config(text="Too low")
    elif guess > n:
        result_label.config(text="Too high!")
    else:
        result_label.config(text="You guessed it right Congratulations !!")
        guess_entry.config(state='disabled')
        submit_button.config(state='disabled')

n = random.randrange(1, 20)

root = tk.Tk()
root.title("Number Guessing Game")

canvas = tk.Canvas(root, width=500, height=300)
canvas.pack()

guess_label = tk.Label(root, text="Enter any number:")
guess_label.place(x=50, y=50)

guess_entry = tk.Entry(root)
guess_entry.place(x=200, y=50)

submit_button = tk.Button(root, text="Submit", command=check_guess)
submit_button.place(x=150, y=100)

result_label = tk.Label(root, text="")
result_label.place(x=150, y=150)

root.mainloop()

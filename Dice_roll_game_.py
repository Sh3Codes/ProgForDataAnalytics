import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import time
import subprocess

class DiceGame:
    def __init__(self, root):
        self.root = root
        self.correct_guesses = 0  
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Dice Guessing Game")

        self.canvas = tk.Canvas(self.root, width=250, height=200, bg="black")
        self.canvas.pack(pady=10)

        self.score_label = tk.Label(self.root, text="Score: 0/0 | Tries left: 7", font=("Arial", 14), fg="red")
        self.score_label.pack(pady=5)

        self.play_button = tk.Button(self.root, text="Play", command=self.play_game, font=("Arial", 12), fg="blue")
        self.play_button.pack(pady=5)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.save_score_and_exit, font=("Arial", 12), fg="blue")
        self.quit_button.pack(pady=5)

    def play_game(self):
        while True:
            self.canvas.delete("all")

            number_of_tries = 7
            while number_of_tries > 0:
                guess = simpledialog.askinteger("Guess the Dice Number", "Enter your guess (1-6):")
                if guess is None:  # User canceled the prompt
                    break
                elif 1 <= guess <= 6:
                    dice_roll = random.randint(1, 6)
                    self.roll_dice_animation()
                    self.display_message(f"The dice rolled: {dice_roll}")

                    if guess == dice_roll:
                        self.correct_guesses += 1
                        self.display_message("Congratulations! You guessed it right!")
                        break
                    else:
                        self.display_message("Sorry, wrong guess. Try again.")
                        number_of_tries -= 1
                else:
                    self.display_message("Invalid input! Please enter a number between 1 and 6.")

                self.update_score_label(number_of_tries)

            if guess is None:  # User canceled the prompt
                break

            if number_of_tries == 0:
                self.display_message("You've used all your tries. Better luck next time!")

            play_again = messagebox.askyesno("Play Again?", "Do you want to play again?")
            if not play_again:
                break

    def update_score_label(self, tries):
        total_tries = 7
        self.score_label.config(text=f"Score: {self.correct_guesses}/{total_tries - tries} | Tries left: {tries}")

    def display_message(self, message):
        messagebox.showinfo("Game Message", message)

    def roll_dice_animation(self):
        for _ in range(10):
            for i in range(1, 7):
                self.canvas.delete("dice")
                self.canvas.create_rectangle(0, 0, 100, 100, fill="black", outline="black", tags="dice")
                self.draw_dice_face(i)
                self.root.update()
                time.sleep(0.05)

    def draw_dice_face(self, number):
        x = self.canvas.winfo_width() / 2
        y = self.canvas.winfo_height() / 2
        radius = 10
        if number % 2 == 1:
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="red", tags="dice")
        if number > 1:
            self.canvas.create_oval(x - 3 * radius, y - 3 * radius, x - radius, y - radius, fill="red", tags="dice")
            self.canvas.create_oval(x + radius, y + radius, x + 3 * radius, y + 3 * radius, fill="red", tags="dice")
        if number > 3:
            self.canvas.create_oval(x + radius, y - 3 * radius, x + 3 * radius, y - radius, fill="red", tags="dice")
            self.canvas.create_oval(x - 3 * radius, y + radius, x - radius, y + 3 * radius, fill="red", tags="dice")
        if number == 6:
            self.canvas.create_oval(x - 3 * radius, y - radius, x - radius, y + radius, fill="red", tags="dice")
            self.canvas.create_oval(x + radius, y - radius, x + 3 * radius, y + radius, fill="red", tags="dice")

    def save_score_and_exit(self):
        try:
            score_exists = False
            try:
                with open("scores.txt", "r") as file:
                    lines = file.readlines()
                    for i, line in enumerate(lines):
                        if line.startswith("Avant's score:"):
                            lines[i] = f"Avant's score: {self.correct_guesses}\n"
                            score_exists = True
                            break
            except FileNotFoundError:
                lines = []

            if score_exists:
                with open("scores.txt", "w") as file:
                    file.writelines(lines)
            else:
                with open("scores.txt", "a") as file:
                    file.write(f"Avant's score: {self.correct_guesses}\n")

        except Exception as e:
            print("An error occurred while saving the score:", e)
        finally:
            self.root.destroy()
            subprocess.Popen(["python", "Main.py"])

def main():
    root = tk.Tk()
    game = DiceGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

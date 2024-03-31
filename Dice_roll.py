import tkinter as tk
from tkinter import simpledialog
import random
import time

class DiceGame:
    def __init__(self, root):
        self.root = root
        self.score = 0
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Dice Guessing Game")

        self.canvas = tk.Canvas(self.root, width=100, height=100)
        self.canvas.pack(pady=10)

        self.score_label = tk.Label(self.root, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(pady=5)

        self.play_button = tk.Button(self.root, text="Play", command=self.play_game, font=("Arial", 12))
        self.play_button.pack(pady=5)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy, font=("Arial", 12))
        self.quit_button.pack(pady=5)

    def play_game(self):
        if self.score == 2:
            self.display_message("You've already won twice! Restart the game to play again.")
            return

        self.canvas.delete("all")  # Clear previous drawings

        number_of_tries = 5
        while number_of_tries > 0:
            guess = simpledialog.askinteger("Guess the Dice Number", "Enter your guess (1-6):")
            if guess is not None and 1 <= guess <= 6:
                dice_roll = random.randint(1, 6)
                self.roll_dice_animation()
                self.display_message(f"The dice rolled: {dice_roll}")

                if guess == dice_roll:
                    self.score += 1
                    self.update_score_label()
                    self.display_message("Congratulations! You guessed it right!")
                    break
                else:
                    self.display_message("Sorry, wrong guess. Try again.")
                    number_of_tries -= 1
            else:
                self.display_message("Invalid input! Please enter a number between 1 and 6.")

        if number_of_tries == 0:
            self.display_message("You've used all your tries. Better luck next time!")

    def update_score_label(self):
        self.score_label.config(text=f"Score: {self.score}")

    def display_message(self, message):
        simpledialog.messagebox.showinfo("Game Message", message)

    def roll_dice_animation(self):
        for _ in range(10):
            for i in range(1, 7):
                self.canvas.delete("dice")
                self.canvas.create_rectangle(0, 0, 100, 100, fill="white", outline="black", tags="dice")
                self.draw_dice_face(i)
                self.root.update()
                time.sleep(0.05)

    def draw_dice_face(self, number):
        x = 50
        y = 50
        radius = 10
        if number % 2 == 1:  # Center dot for odd numbers
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="black", tags="dice")
        if number > 1:  # Top-left and bottom-right dots for 2 and 3
            self.canvas.create_oval(x - 3 * radius, y - 3 * radius, x - radius, y - radius, fill="black", tags="dice")
            self.canvas.create_oval(x + radius, y + radius, x + 3 * radius, y + 3 * radius, fill="black", tags="dice")
        if number > 3:  # Top-right and bottom-left dots for 4, 5, and 6
            self.canvas.create_oval(x + radius, y - 3 * radius, x + 3 * radius, y - radius, fill="black", tags="dice")
            self.canvas.create_oval(x - 3 * radius, y + radius, x - radius, y + 3 * radius, fill="black", tags="dice")
        if number == 6:  # Middle-left and middle-right dots for 6
            self.canvas.create_oval(x - 3 * radius, y - radius, x - radius, y + radius, fill="black", tags="dice")
            self.canvas.create_oval(x + radius, y - radius, x + 3 * radius, y + radius, fill="black", tags="dice")

def main():
    root = tk.Tk()
    game = DiceGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

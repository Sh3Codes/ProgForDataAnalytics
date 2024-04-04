import tkinter as tk
from tkinter import font as tkfont
import subprocess
import os

root = None  # Define root at the module level

def launch_slot_machine():
    global root  # Access root defined at the module level
    try:
        subprocess.Popen(["python", "SLOTMACHINENew.py"])
    except Exception as e:
        print("Error launching slot machine game:", e)
    root.destroy()  # Close the main menu when launching a game

def launch_snake_game():
    global root  # Access root defined at the module level
    try:
        subprocess.Popen(["python", "snake_gamepython.py"])
    except Exception as e:
        print("Error launching snake game:", e)
    root.destroy()  # Close the main menu when launching a game
        
def launch_dice_roll_guess():
    global root  # Access root defined at the module level
    try:
        subprocess.Popen(["python", "Dice_roll_game_.py"])
    except Exception as e:
        print("Error launching dice rolling game:", e)
    root.destroy()  # Close the main menu when launching a game

def exit_game():
    try:
        print("Exiting...")
        root.destroy()
        # Delete the scores.txt file if it exists
        if os.path.exists("scores.txt"):
            os.remove("scores.txt")
            print("scores.txt file deleted.")
        else:
            print("scores.txt file does not exist.")
    except Exception as e:
        print("An error occurred while exiting the game:", e)

def read_scores():
    try:
        with open("scores.txt", "r") as file:
            lines = file.readlines()
            scores = {}
            for line in lines:
                name, score = line.strip().split(":")
                scores[name.strip()] = int(score.strip())
            return scores
    except FileNotFoundError:
        return {"Dayjah": 0, "Avant": 0, "Shantal": 0}

def display_scores():
    scores = read_scores()
    average_score = sum(scores.values()) / len(scores)
    for i, (name, score) in enumerate(scores.items()):
        label = tk.Label(root, text=f"{name}'s score: {score}", font=("Helvetica", 12))
        label.pack(pady=5)
    average_label = tk.Label(root, text=f"Average Score: {average_score:.2f}", font=("Helvetica", 12))
    average_label.pack(pady=10)

def main():
    global root
    root = tk.Tk()
    root.title("Game Menu")
    root.configure(bg="#34495e")
    root.geometry("600x400")

    title_font = tkfont.Font(family="Helvetica", size=30, weight="bold")
    button_font = tkfont.Font(family="Helvetica", size=18)

    menu_frame = tk.Frame(root, bg="#34495e")
    menu_frame.pack(expand=True)

    title_label = tk.Label(menu_frame, text="Select a Game", font=title_font, bg="#34495e", fg="#ecf0f1")
    title_label.pack(pady=20)

    slot_button = tk.Button(menu_frame, text="Slot Machine", font=button_font, bg="#3498db", fg="#ecf0f1", command=launch_slot_machine)
    slot_button.pack(pady=10, padx=50, ipadx=20, ipady=10, fill=tk.BOTH)

    snake_button = tk.Button(menu_frame, text="Snake Game", font=button_font, bg="#2ecc71", fg="#ecf0f1", command=launch_snake_game)
    snake_button.pack(pady=10, padx=50, ipadx=20, ipady=10, fill=tk.BOTH)

    dice_button = tk.Button(menu_frame, text="Dice Roll Guess", font=button_font, bg="#e67e22", fg="#ecf0f1", command=launch_dice_roll_guess)
    dice_button.pack(pady=10, padx=50, ipadx=20, ipady=10, fill=tk.BOTH)

    scores_button = tk.Button(menu_frame, text="Display Scores", font=button_font, bg="#f39c12", fg="#ecf0f1", command=display_scores)
    scores_button.pack(pady=10, padx=50, ipadx=20, ipady=10, fill=tk.BOTH)

    exit_button = tk.Button(menu_frame, text="Exit", font=button_font, bg="#e74c3c", fg="#ecf0f1", command=exit_game)
    exit_button.pack(pady=10, padx=50, ipadx=20, ipady=10, fill=tk.BOTH)

    root.mainloop()

if __name__ == "__main__":
    main()


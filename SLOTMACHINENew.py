import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import time
import winsound
import subprocess


MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
}

symbol_colors = {
    "A": "red",
    "B": "green",
    "C": "blue",
    "D": "orange",
}

class SlotMachineGame:
    def __init__(self, root):
        self.root = root
        self.balance = 0
        self.score = self.load_score()  # Initialize score by loading from the file
        self.setup_ui()
        self.load_sounds()

    def load_score(self):
        try:
            with open("scores.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("Dayjah's score"):
                        return int(line.split(":")[1].strip())
        except FileNotFoundError:
            print("Scores file not found.")
        except Exception as e:
            print("An error occurred while loading the score:", e)
        return 0  # Return 0 if score loading fails or file not found


    def load_sounds(self):
        self.spin_sound = "spin.wav"
        self.win_sound = "win.wav"
        self.loss_sound = "loss.wav"
        self.game_sound = "game.wav"
        winsound.PlaySound(self.spin_sound, winsound.SND_ASYNC)
        winsound.PlaySound(self.win_sound, winsound.SND_ASYNC)
        winsound.PlaySound(self.loss_sound, winsound.SND_ASYNC)
        winsound.PlaySound(self.game_sound, winsound.SND_ASYNC)

    def setup_ui(self):
        self.root.title("Slot Machine Game")
        self.root.configure(bg="black")

        self.canvas = tk.Canvas(self.root, width=300, height=200, bg="black")
        self.canvas.pack(pady=10)

        self.balance_label = tk.Label(self.root, text="Balance: $0", font=("Arial", 14), bg="black", fg="white")
        self.balance_label.pack()

        # Add score label
        self.score_label = tk.Label(self.root, text="Score: 0", font=("Arial", 14), bg="black", fg="white")
        self.score_label.pack()

        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack()

        self.deposit_button = tk.Button(button_frame, text="Deposit", command=self.deposit, font=("Arial", 12), bg="blue", fg="white", width=10)
        self.deposit_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.spin_button = tk.Button(button_frame, text="Spin", command=self.spin, font=("Arial", 12), bg="yellow", fg="black", width=10)
        self.spin_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.exit_button = tk.Button(button_frame, text="Exit", command=self.save_score_and_exit, font=("Arial", 12), bg="red", fg="white", width=10)
        self.exit_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12), bg="black", fg="white")
        self.result_label.pack(pady=10)
        
        self.update_spin_button()

    def deposit(self):
        amount = simpledialog.askinteger("Deposit", "Enter deposit amount:")
        if amount is not None and amount > 0:
            self.balance += amount
            self.update_balance_label()
            self.update_spin_button()

    def get_number_of_lines(self):
        while True:
            lines = simpledialog.askinteger("Number of Lines", f"Enter number of lines (1-{MAX_LINES}):")
            if lines is not None:
                if 1 <= lines <= MAX_LINES:
                    return lines
                else:
                    simpledialog.messagebox.showwarning("Out of Range", f"Number of lines must be between 1 and {MAX_LINES}. Please try again.")
            else:
                return None


    def get_bet(self):
        while True:
            bet = simpledialog.askinteger("Bet Amount", f"Enter bet amount (${MIN_BET}-${MAX_BET}):")
            if bet is not None:
                if MIN_BET <= bet <= MAX_BET:
                    return bet
                else:
                    simpledialog.messagebox.showwarning("Out of Range", f"Bet amount must be between ${MIN_BET} and ${MAX_BET}. Please try again.")
            else:
                return None


    def spin(self):
        self.result_label.config(text="")
        lines = self.get_number_of_lines()
        if lines is None:
            return

        bet = self.get_bet()
        if bet is None:
            return

        total_bet = bet * lines
        if total_bet > self.balance:
            self.result_label.config(text=f"Not enough balance to bet ${total_bet}")
            return

        self.balance -= total_bet
        self.update_balance_label()

        self.animate_spin(lines, bet)

    def animate_spin(self, lines, bet):
        winsound.PlaySound(self.spin_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)  # Play spin sound
        reels = []
        for i in range(COLS):
            reel = [random.choice(list(symbol_count.keys())) for _ in range(ROWS)]
            reels.append(reel)

        for _ in range(10):
            for i in range(COLS):
                reel = reels[i]
                random.shuffle(reel)
                self.display_reel(reel, i)
                time.sleep(0.1)
                self.root.update()

        for _ in range(10):
            for i in range(COLS):
                reel = reels[i]
                random.shuffle(reel)
                self.display_reel(reel, i)
                time.sleep(0.05)
                self.root.update()

        slots = [reel[:lines] for reel in reels]
        self.display_slot_machine(slots)

        winnings, _ = self.check_winnings(slots, lines, bet, symbol_value)
        if winnings > 0:
            self.balance += winnings
            self.update_balance_label()
            self.score += 1  # Increase score
            self.update_score_label()  # Update score label
            self.result_label.config(text=f"Congratulations! You won ${winnings}!")
            winsound.PlaySound(self.win_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)  # Play win sound
        else:
            self.result_label.config(text="Sorry, you didn't win anything.")
            winsound.PlaySound(self.loss_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)  # Play loss sound

        self.update_spin_button()

    def display_reel(self, reel, col):
        for i, symbol in enumerate(reel):
            x1, y1 = col * 100, i * 50
            x2, y2 = x1 + 100, y1 + 50
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=symbol_colors[symbol])
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=symbol, fill="white", font=("Arial", 14))

    def display_slot_machine(self, columns):
        display_text = ""
        for row in range(len(columns[0])):
            for i, column in enumerate(columns):
                if i != len(columns) - 1:
                    display_text += column[row] + " | "
                else:
                    display_text += column[row] + "\n"
        self.result_label.config(text=display_text)

    def check_winnings(self, columns, lines, bet, values):
        winnings = 0
        winning_lines = []

        for line in range(lines):
            symbols_in_line = [column[line] for column in columns]
            if len(set(symbols_in_line)) == 1:
                symbol = symbols_in_line[0]
                winnings += symbol_value[symbol] * bet
                winning_lines.append(line + 1)

        if len(winning_lines) == lines:
            winnings *= lines

        return winnings, winning_lines

    def update_balance_label(self):
        self.balance_label.config(text=f"Balance: ${self.balance}")

    def update_score_label(self):
        self.score_label.config(text=f"Score: {self.score}")

    def update_spin_button(self):
        if self.balance <= 0:
            self.spin_button.config(state="disabled")
        else:
            self.spin_button.config(state="normal")
            
    def save_score_and_exit(self):
        try:
            with open("scores.txt", "a") as file:
                file.write(f"Dayjah's score: {self.score}\n")  # Append in a new line
        except Exception as e:
            print("An error occurred while saving the score:", e)
        finally:
            self.root.destroy()
            subprocess.Popen(["python", "Main.py"])

def main():
    root = tk.Tk()
    game = SlotMachineGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

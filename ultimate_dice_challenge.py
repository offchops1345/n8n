import random
import tkinter as tk
from tkinter import messagebox

class DiceGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Ultimate Dice Challenge")
        self.player_scores = {}
        self.current_player = None
        self.current_score = 0
        self.locked_dice = []
        self.target_score = 20000

        self.create_setup_screen()

    def create_setup_screen(self):
        self.setup_frame = tk.Frame(self.master)
        self.setup_frame.pack(pady=20)

        self.entry_label = tk.Label(self.setup_frame, text="Enter Player Name:")
        self.entry_label.pack(side=tk.LEFT)

        self.player_name_entry = tk.Entry(self.setup_frame)
        self.player_name_entry.pack(side=tk.LEFT, padx=5)

        self.add_player_button = tk.Button(self.setup_frame, text="Add Player", command=self.add_player)
        self.add_player_button.pack(side=tk.LEFT)

        self.start_game_button = tk.Button(self.master, text="Start Game", command=self.start_game)
        self.start_game_button.pack(pady=20)

        self.player_list_label = tk.Label(self.master, text="No players added yet.")
        self.player_list_label.pack(pady=20)

    def add_player(self):
        player_name = self.player_name_entry.get()
        if player_name and player_name not in self.player_scores:
            self.player_scores[player_name] = self.target_score
            self.player_name_entry.delete(0, tk.END)
            self.player_list_label.config(text=f"Players: {', '.join(self.player_scores.keys())}")
            messagebox.showinfo("Player Added", f"{player_name} has been added!")
        else:
            messagebox.showwarning("Warning", "Invalid player name or player already exists!")

    def start_game(self):
        if len(self.player_scores) < 2:
            messagebox.showwarning("Warning", "Please add at least two players before starting the game.")
            return
        
        self.current_player = list(self.player_scores.keys())[0]
        self.current_score = 0
        self.locked_dice = []
        self.update_game_screen()
        self.roll_dice()

    def roll_dice(self):
        roll = [random.randint(1, 6) for _ in range(5)]
        self.display_dice(roll)

    def display_dice(self, roll):
        if hasattr(self, 'dice_frame'):
            self.dice_frame.destroy()

        self.dice_frame = tk.Frame(self.master)
        self.dice_frame.pack(pady=20)
        
        for i, die in enumerate(roll):
            button = tk.Button(self.dice_frame, text=str(die), width=5, height=2, 
                               command=lambda d=die: self.lock_dice(d, roll))
            button.grid(row=0, column=i, padx=5)

        self.roll_button = tk.Button(self.master, text="Roll Again", command=self.roll_dice)
        self.roll_button.pack(pady=20)

    def lock_dice(self, die, roll):
        if die not in self.locked_dice:
            self.locked_dice.append(die)
            messagebox.showinfo("Dice Locked", f"You have locked in the die: {die}")

            round_points = self.calculate_score(roll)

            if round_points > 0:
                self.current_score += round_points
                messagebox.showinfo("Score Update", f"Current Score: {self.current_score}")

            if len(self.locked_dice) == 5:
                self.end_turn()  # Automatically end turn if all dice are locked

        else:
            messagebox.showwarning("Warning", "You have already locked in this die.")

    def calculate_score(self, roll):
        score = 0
        counts = {die: roll.count(die) for die in set(roll)}

        # Individual scoring
        score += counts.get(1, 0) * 100
        score += counts.get(5, 0) * 50

        # Three of a Kind & Full House
        for die, count in counts.items():
            if count >= 3:
                score += die * 100
                if die == 1:
                    score += 700  # Bonus for three of a kind of '1's
                if count > 3:
                    score += die * 100  # Bonus for four of a kind
                if count == 5:
                    score += die * 1000  # Bonus for five of a kind
            if count == 2 and list(counts.values()).count(3) > 0:
                score += 1000  # Full House

        # Check for Straight
        if sorted(roll) == [1, 2, 3, 4, 5]:
            score += 1500  # Straight score
            
        return score

    def end_turn(self):
        self.player_scores[self.current_player] -= self.current_score
        if self.player_scores[self.current_player] <= 0:
            messagebox.showinfo("Winner!", f"{self.current_player} wins!")
            self.reset_game()
        else:
            players = list(self.player_scores.keys())
            current_index = players.index(self.current_player)
            self.current_player = players[(current_index + 1) % len(players)]
            self.update_game_screen()
            self.locked_dice = []
            self.current_score = 0
            messagebox.showinfo("Next Turn", f"{self.current_player}'s turn!")
            self.roll_dice()

    def update_game_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.score_label = tk.Label(self.master, text=f"{self.current_player}'s Turn!", font=('Arial', 16))
        self.score_label.pack(pady=10)

        score_display = "\n".join([f"{player}: {score}" for player, score in self.player_scores.items()])
        self.scores_label = tk.Label(self.master, text=f"Scores:\n{score_display}", font=('Arial', 14))
        self.scores_label.pack(pady=10)

        self.roll_button = tk.Button(self.master, text="Roll Dice", command=self.roll_dice, font=('Arial', 14))
        self.roll_button.pack(pady=10)

        self.reset_button = tk.Button(self.master, text="Reset Game", command=self.reset_game, font=('Arial', 14))
        self.reset_button.pack(pady=10)

    def reset_game(self):
        self.player_scores = {}
        self.current_player = None
        self.current_score = 0
        self.locked_dice = []
        self.create_setup_screen()
        messagebox.showinfo("Game Reset", "The game has been reset!")

if __name__ == "__main__":
    root = tk.Tk()
    game = DiceGame(root)
    root.mainloop()
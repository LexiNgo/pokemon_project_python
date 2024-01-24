import tkinter as tk
from tkinter import ttk
import subprocess
import requests

class PokemonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application Pokémon")
        self.root.geometry("300x200")  # Set initial window size
        self.root.minsize(300, 200)  # Set minimum window size

        # Create a frame to hold the buttons
        frame = ttk.Frame(root, padding="30 15")  # Add some padding around the frame
        frame.pack(fill=tk.BOTH, expand=True)

        # Create the buttons with some padding around them
        self.button_pokedex = ttk.Button(frame, text="Pokédex", command=self.run_pokedex_script)
        self.button_pokedex.pack(pady=10)

        self.button_combat = ttk.Button(frame, text="Combat", command=self.run_combat_script)
        self.button_combat.pack(pady=10)

    def run_pokedex_script(self):
        subprocess.run(["python", "pokedex/pokedex.py"])

    def run_combat_script(self):
        subprocess.run(["python", "pokedex/combat.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonApp(root)
    root.mainloop()
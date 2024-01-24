import tkinter as tk
from tkinter import *
import requests
from tkinter import ttk
from pokedex import Pokemon
from damage_calculus import calculate_damage
from PIL import Image, ImageTk
import io


class BattleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pokemon Battle")
        self.root.geometry("1200x800")  # Adjust the size as needed
        self.pokemon1_name = tk.StringVar()
        self.pokemon2_name = tk.StringVar()

        all_pokemon_names = Pokemon().get_all_pokemon_names()

        # Create dropdown menus for selecting Pokemon
        self.pokemon1_dropdown = ttk.Combobox(self.root, textvariable=self.pokemon1_name, values=all_pokemon_names)
        self.pokemon2_dropdown = ttk.Combobox(self.root, textvariable=self.pokemon2_name, values=all_pokemon_names)

        # Create frames for each Pokemon
        self.pokemon1_frame = tk.Frame(self.root)
        self.pokemon2_frame = tk.Frame(self.root)

        # Create labels for Pokemon sprites, names, and HP
        self.pokemon1_sprite = tk.Label(self.pokemon1_frame)
        self.pokemon2_sprite = tk.Label(self.pokemon2_frame)
        self.pokemon1_name_label = tk.Label(self.pokemon1_frame, textvariable=self.pokemon1_name)
        self.pokemon2_name_label = tk.Label(self.pokemon2_frame, textvariable=self.pokemon2_name)
        self.pokemon1_hp_label = tk.Label(self.pokemon1_frame)
        self.pokemon2_hp_label = tk.Label(self.pokemon2_frame)

        # Pack the labels into the frames
        self.pokemon1_sprite.pack()
        self.pokemon1_name_label.pack()
        self.pokemon1_hp_label.pack()
        self.pokemon2_sprite.pack()
        self.pokemon2_name_label.pack()
        self.pokemon2_hp_label.pack()

        # Create buttons for starting the battle, proceeding to the next turn, and restarting the battle
        self.start_button = tk.Button(self.root, text="Start Battle", command=self.start_battle)
        self.next_turn_button = tk.Button(self.root, text="Next Turn", command=self.next_turn)
        self.restart_button = tk.Button(self.root, text="Reset Battle", command=self.reset_battle)
        self.restart_button.pack_forget()  # Hide the button until the battle starts

        # Create a text box for the battle log
        self.battle_log = tk.Text(self.root)

        # Place the widgets
        self.pokemon1_dropdown.pack()
        self.pokemon2_dropdown.pack()
        self.start_button.pack()
        self.next_turn_button.pack()  # Pack the next turn button before the restart button
        self.restart_button.pack()  # Pack the restart button after the next turn button
        self.pokemon1_frame.pack(side="left")  # Adjust the position as needed
        self.pokemon2_frame.pack(side="right")  # Adjust the position as needed
        self.battle_log.pack()
        self.root.mainloop()


    def log_message(self, message):
        self.battle_log.insert(tk.END, message + "\n")

    def start_battle(self):
        pokemon1_name = self.pokemon1_name.get()
        pokemon2_name = self.pokemon2_name.get()
        self.pokemon1 = Pokemon(pokemon1_name)
        self.pokemon2 = Pokemon(pokemon2_name)
        self.pokemon1_details = self.pokemon1.details
        self.pokemon2_details = self.pokemon2.details

        for sprite_label, pokemon_details in [(self.pokemon1_sprite, self.pokemon1_details), (self.pokemon2_sprite, self.pokemon2_details)]:
            # Get the image from the URL
            response = requests.get(pokemon_details['sprites']['front_default'])
            image_data = response.content

            # Create an Image object from the image data
            image = Image.open(io.BytesIO(image_data))

            # Create a PhotoImage object that can be displayed in a Label widget
            photo = ImageTk.PhotoImage(image)

            # Update the image in the label
            sprite_label.config(image=photo)
            sprite_label.image = photo  # Keep a reference to the image to prevent it from being garbage collected
            sprite_label.pack()

        self.pokemon1_name_label.config(text=self.pokemon1_name.get())
        self.pokemon2_name_label.config(text=self.pokemon2_name.get())
        self.pokemon1_hp_label.config(text=f"HP: {self.pokemon1_details['stats'][0]['base_stat']}")
        self.pokemon2_hp_label.config(text=f"HP: {self.pokemon2_details['stats'][0]['base_stat']}")
        self.pokemon1_name_label.pack()
        self.pokemon2_name_label.pack()
        self.pokemon1_hp_label.pack()
        self.pokemon2_hp_label.pack()

        self.restart_button.pack()
        # Get the speed from the stats
        pokemon1_speed = self.pokemon1_details['stats'][5]['base_stat']
        pokemon2_speed = self.pokemon2_details['stats'][5]['base_stat']

        # Determine the order of attack based on speed
        if pokemon1_speed >= pokemon2_speed:
            self.first_attacker, self.second_attacker = self.pokemon1_details, self.pokemon2_details
            self.first_name, self.second_name = pokemon1_name, pokemon2_name
        else:
            self.first_attacker, self.second_attacker = self.pokemon2_details, self.pokemon1_details
            self.first_name, self.second_name = pokemon2_name, pokemon1_name

        self.battle_turn = BattleTurn(self.first_attacker, self.second_attacker, self.first_name, self.second_name, self.log_message, self.next_turn_button, self.root)
        # Show the next turn button
        self.next_turn_button.pack()
        self.restart_button.pack()

    def next_turn(self):
        # Check if either Pokemon's HP has reached 0
        if self.pokemon1_details['stats'][0]['base_stat'] <= 0 or self.pokemon2_details['stats'][0]['base_stat'] <= 0:
            # Disable the "Next Turn" button
            self.next_turn_button.config(state='disabled')
            return

        # Execute the next turn of the battle
        self.battle_turn.execute_turn()

        # Update the HP values
        self.pokemon1_details['stats'][0]['base_stat'] = self.first_attacker['stats'][0]['base_stat']
        self.pokemon2_details['stats'][0]['base_stat'] = self.second_attacker['stats'][0]['base_stat']

        # Update the HP labels
        self.pokemon1_hp_label.config(text=f"HP: {self.pokemon1_details['stats'][0]['base_stat']}")
        self.pokemon2_hp_label.config(text=f"HP: {self.pokemon2_details['stats'][0]['base_stat']}")


    def reset_battle(self):
        # Reset the Pokemon details
        self.pokemon1_details = None
        self.pokemon2_details = None

        # Reset the HP labels
        self.pokemon1_hp_label.config(text="HP: ")
        self.pokemon2_hp_label.config(text="HP: ")

        # Reset the name labels
        self.pokemon1_name_label.config(text="")
        self.pokemon2_name_label.config(text="")

        # Unpack the next turn and restart buttons
        self.next_turn_button.pack_forget()
        self.restart_button.pack_forget()

        # Enable the "Next Turn" button
        self.next_turn_button.config(state='normal')

        # Clear the battle log
        self.battle_log.delete('1.0', END)

        # Start a new battle
        self.start_battle()

#before optimization
        

        
class BattleTurn:
    def __init__(self, first_attacker, second_attacker, first_name, second_name, log_message, next_turn_button, root):
        self.first_attacker = first_attacker
        self.second_attacker = second_attacker
        self.first_name = first_name
        self.second_name = second_name
        self.log_message = log_message
        self.next_turn_button = next_turn_button
        self.root = root

    def execute_turn(self):
        # First attacker attacks second attacker
        self.attack_and_log(self.first_attacker, self.second_attacker, self.first_name, self.second_name)

        # If second attacker is still alive, it attacks the first attacker
        if self.second_attacker['stats'][0]['base_stat'] > 0:
            self.attack_and_log(self.second_attacker, self.first_attacker, self.second_name, self.first_name)

        # Determine the winner
        if self.first_attacker['stats'][0]['base_stat'] <= 0:
            self.log_message(f"{self.second_name} a gagné !")
        elif self.second_attacker['stats'][0]['base_stat'] <= 0:
            self.log_message(f"{self.first_name} a gagné !")

        # If there's a winner, disable the "Next Turn" button
        if self.first_attacker['stats'][0]['base_stat'] <= 0 or self.second_attacker['stats'][0]['base_stat'] <= 0:
            self.next_turn_button.config(state='disabled')
            self.root.update()

    def attack_and_log(self, attacker, defender, attacker_name, defender_name):
        damage = calculate_damage(attacker, defender)
        defender['stats'][0]['base_stat'] -= damage
        defender['stats'][0]['base_stat'] = max(0, defender['stats'][0]['base_stat'])  # Ensure HP doesn't go below 0
        self.log_message(f"{attacker_name} attaque {defender_name} et lui a fait {damage} damage, il reste {defender['stats'][0]['base_stat']} HP à {defender_name}.")
# Create an instance of BattleApp to start the battle simulation
app = BattleApp()
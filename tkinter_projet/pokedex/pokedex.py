import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io


class Pokemon:
    def __init__(self, name=None):
        self.name = name
        self.details = self.get_details() if name else None
        self.details_text = None
        self.details_image_label = None
        self.search_entry = None
        self.pokemon_combobox = None

    def get_all_pokemon_names(self):
        url = "https://pokeapi.co/api/v2/pokemon?limit=151"
        response = requests.get(url)
        data = response.json()
        all_pokemon_names = [pokemon["name"] for pokemon in data["results"]]
        return all_pokemon_names

    def get_details(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.name}"
        response = requests.get(url)
        data = response.json()
        return data

    def filter_pokemon(self, event):
        search_term = self.search_entry.get().lower()
        all_pokemon_names = self.get_all_pokemon_names()
        filtered_pokemon = [pokemon for pokemon in all_pokemon_names if pokemon.startswith(search_term)]
        self.pokemon_combobox.config(values=filtered_pokemon)

    def show_pokemon_details(self, event):
        name = self.pokemon_combobox.get()
        pokemon = Pokemon(name)
        details = pokemon.details

        stats = "\n".join(
            f"{stat['stat']['name'].title()}: {stat['base_stat']}"
            for stat in details['stats']
        )

        self.details_text.set(
            f"Name: {details['name'].title()}\n"
            f"Height: {details['height']}\n"
            f"Weight: {details['weight']}\n"
            f"Type: {details['types'][0]['type']['name'].title()}\n"
            f"Stats: \n{stats}"
        )

        # Get the image from the URL
        response = requests.get(details['sprites']['front_default'])
        image_data = response.content

        # Create an Image object from the image data
        image = Image.open(io.BytesIO(image_data))

        # Create a PhotoImage object that can be displayed in a Label widget
        photo = ImageTk.PhotoImage(image)

        # Update the image in the label
        self.details_image_label.config(image=photo)
        self.details_image_label.image = photo  # Keep a reference to the image to prevent it from being garbage collected

    def clear_search_bar(self, event):
        self.search_entry.delete(0, 'end')


    def create_pokedex_window(self):
        window = tk.Tk()
        window.title("Pokémon Details")
        window.geometry("500x500")

        self.details_text = tk.StringVar()

        all_pokemon_names = self.get_all_pokemon_names()

        self.search_entry = ttk.Entry(window, font=("Arial", 12))
        self.search_entry.insert(0, 'Rechercher')  # Set initial text
        self.search_entry.bind('<FocusIn>', self.clear_search_bar)  # Clear text when the search bar is clicked
        self.search_entry.pack(pady=10)
        self.search_entry.bind("<KeyRelease>", self.filter_pokemon)

        self.pokemon_combobox = ttk.Combobox(window, values=all_pokemon_names)
        self.pokemon_combobox.set("Choose a Pokémon")
        self.pokemon_combobox.bind("<<ComboboxSelected>>", self.show_pokemon_details)

        self.details_image_label = ttk.Label(window)
        self.details_image_label.pack(pady=10)

        name_label = ttk.Label(window, textvariable=self.details_text, font=("Arial", 20))  # Increase the font size as needed
        name_label.pack(pady=10)

        details_label = ttk.Label(window, textvariable=self.details_text, font=("Arial", 12))
        details_label.pack(pady=10)

        self.pokemon_combobox.pack(pady=10)

        window.mainloop()


if __name__ == "__main__":
    pokedex = Pokemon()
    pokedex.create_pokedex_window()
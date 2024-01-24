import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from dbConnect import curseur, connexion

class Team:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pokemon Team")
        self.root.geometry("1200x800")

        team_names = [name for id, name in self.get_all_team_names()]

        self.team_name_1 = tk.StringVar()
        self.team_dropdown_1 = ttk.Combobox(self.root, textvariable=self.team_name_1, values=team_names)
        self.team_dropdown_1.pack()
        self.team_dropdown_1.bind("<<ComboboxSelected>>", self.update_pokemon_display_1)
        
        self.team_name_2 = tk.StringVar()
        self.team_dropdown_2 = ttk.Combobox(self.root, textvariable=self.team_name_2, values=team_names)
        self.team_dropdown_2.pack()
        self.team_dropdown_2.bind("<<ComboboxSelected>>", self.update_pokemon_display_2)

        self.pokemon_frame_team_1 = tk.Frame(self.root)
        self.pokemon_frame_team_1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.pokemon_frame_team_2 = tk.Frame(self.root)
        self.pokemon_frame_team_2.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.root.mainloop()
        

    def get_all_team_names(self):
        curseur.execute("SELECT id, name FROM team_team")
        teams = [(id, name) for id, name in curseur.fetchall()]
        return teams

    
    def get_all_team_id(self):
        curseur.execute("SELECT id FROM team_team")
        ids = []
        for id in curseur :
            ids.append(id)
        connexion.close()
        return ids
    
    
    def get_all_pokemon_team_id(self,id: int):
        curseur.execute("SELECT pokemon_id FROM team_team_pokemons WHEN team_id= ?", id)
        for idp in curseur :
            self.pokemons = self.pokemons[idp]
        connexion.close()
        return self.pokemons
    
    def get_num_pokemon(self, team_id):
        curseur.execute("SELECT number FROM pokedex_pokemon INNER JOIN team_team_pokemons ON pokedex_pokemon.id = team_team_pokemons.pokemon_id WHERE team_id=?", (team_id,))
        pokemon_ids = [pid[0] for pid in curseur.fetchall()]
        return pokemon_ids

    
    def update_pokemon_display_1(self, event=None):
        selected_index = self.team_dropdown_1.current()
        if selected_index < 0:
            return
        team_id = self.get_all_team_names()[selected_index][0]
        self.update_pokemon_display(team_id, self.pokemon_frame_team_1)

    def update_pokemon_display_2(self, event=None):
        selected_index = self.team_dropdown_2.current()
        if selected_index < 0:
            return
        team_id = self.get_all_team_names()[selected_index][0]
        self.update_pokemon_display(team_id, self.pokemon_frame_team_2)

    def update_pokemon_display(self, team_id, pokemon_frame):
        pokemon_ids = self.get_num_pokemon(team_id)
        
        for widget in pokemon_frame.winfo_children():
            widget.destroy()

        for pid in pokemon_ids:
            pokemon_data = self.get_pokemon_data(pid)
            if pokemon_data:
                pokemon_frame_individual = tk.Frame(pokemon_frame)
                pokemon_frame_individual.pack()

                pokemon_name_label = tk.Label(pokemon_frame_individual, text=pokemon_data['name'])
                pokemon_name_label.pack()

                image_url = pokemon_data['image_url']
                image_response = requests.get(image_url)
                image_data = Image.open(BytesIO(image_response.content))
                max_size = (100, 100)
                image_data.thumbnail(max_size)
                photo = ImageTk.PhotoImage(image_data)

                pokemon_image_label = tk.Label(pokemon_frame_individual, image=photo)
                pokemon_image_label.image = photo
                pokemon_image_label.pack()

    def get_pokemon_data(self, pokemon_id):
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            pokemon_name = data['name']
            pokemon_image_url = data['sprites']['other']['official-artwork']['front_default']
            return {'name': pokemon_name, 'image_url': pokemon_image_url}
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des données du Pokémon : {e}")
            return None
        
team = Team() 
from django.db import models
import requests

class Attack(models.Model):
    name = models.CharField(max_length=50)
    attack_type = models.CharField(max_length=20)
    power = models.PositiveSmallIntegerField()
    status_effect = models.CharField(max_length=20, blank=True, null=True) 
    status_effect_chance = models.FloatField(default=0)
    status_change = models.CharField(max_length=50, blank=True, null=True)
    stat_change = models.IntegerField(blank=True, null=True) 
    stat_change_target = models.CharField(max_length=10, default="self")

    def __str__(self):
        status_part = f", Status Effect: {self.status_effect}" if self.status_effect else ""
        return f"{self.name} ({self.attack_type}, Power: {self.power}{status_part})"
    
    
    @staticmethod
    def saveAttack(attack_names):
        for name in attack_names:
            # Vérifier si l'attaque existe déjà dans la BDD
            if not Attack.objects.filter(name=name).exists():
                # Appel API pour obtenir les informations sur l'attaque
                response = requests.get(f'https://pokeapi.co/api/v2/move/{name}')
                if response.status_code == 200:
                    data = response.json()
                    # Créer une nouvelle instance d'Attack
                    attack = Attack(
                        name=name,
                        attack_type=data['type']['name'],
                        power=data['power'],
                        status_effect=data.get('status_effect', ''),
                        status_effect_chance=data.get('status_effect_chance', 0),
                        status_change=data.get('status_change', ''),
                        stat_change=data.get('stat_change', None),
                        stat_change_target=data.get('stat_change_target', 'self')
                    )
                    attack.save()
    

class Pokemon(models.Model):
    number = models.PositiveSmallIntegerField()
    attacks = models.ManyToManyField(Attack, blank=True) # Liste des objets Attack
    

    def fetch_pokeapi_data(self):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.number_pokedex}")
        if response.status_code == 200:
            data = response.json()
            self.name = data['name']
            self.type1 = data['types'][0]['type']['name']
            if len(data['types']) > 1:
                self.type2 = data['types'][1]['type']['name']
            else:
                self.type2 = None
            self.max_health = data['stats'][0]['base_stat']
            self.current_health = self.max_health 
            self.attack = data['stats'][1]['base_stat']
            self.defense = data['stats'][2]['base_stat']
            self.speed = data['stats'][5]['base_stat']
        else:
            print("Erreur lors de la récupération des données depuis PokeAPI")

        self.is_knocked_out = False
        self.sleep_turns = 0
        self.status_conditions = {
            "poisoned": False, 
            "asleep": False, 
            "paralyzed": False,
            "frozen": False,
            "burned": False
        }
        self.attack_modifier = 0
        self.defense_modifier = 0
        self.speed_modifier = 0

    def fetch_pokeapi_data(self):
        # Utilisez 'self.number' au lieu de 'self.number_pokedex'
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.number}")
        if response.status_code == 200:
            data = response.json()
            # ... le reste de votre logique de traitement des données ...
        else:
            print("Erreur lors de la récupération des données depuis PokeAPI")

    def get_pokemon_details(pokedex_number):
        url = f"https://pokeapi.co/api/v2/pokemon/{pokedex_number}/"
        response = requests.get(url)
        pokemon_details = response.json()

        attacks = pokemon_details['moves']
        attack_names = [attack['move']['name'] for attack in attacks]

        return {
            'number': int(pokemon_details['id']),
            'name': pokemon_details['name'],
            'image': pokemon_details['sprites']['other']['official-artwork']['front_default'],
            'types': [type['type']['name'] for type in pokemon_details['types']],
            'height': pokemon_details['height'],
            'weight': pokemon_details['weight'],
            'stats': [base_stat['stat']['name'] for base_stat in pokemon_details['stats']],
            'stats_of': [{'name': stat['stat']['name'], 'value': stat['base_stat']} for stat in pokemon_details['stats']],
            'attacks': attack_names,
        }

    def __str__(self):
        return self.name

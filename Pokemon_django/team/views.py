from django.shortcuts import get_object_or_404, redirect, render
from .models import Team
import random
import requests
from pokedex.models import Pokemon, Attack
from django.db import IntegrityError

def create_team(request):
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        if team_name:
            Team.createTeam(team_name)
            return redirect('create_team')  
    return render(request, 'create_team.html')  

def delete_team(request, team_name):
    Team.deleteTeam(team_name)
    teams = Team.objects.all()
    for team in teams:
        print(team.name)  # or use logging

    return render(request, 'all_teams.html', {'teams': teams})

def rename_team(request, old_name):
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        if new_name:
            Team.renameTeam(old_name, new_name)
            
    return render(request, 'rename_team.html', {'old_name': old_name})


def clear_pokemons_from_team(request, team_name):
    Team.clearAllPokemonTeam(team_name)
    return redirect('all_teams.html')

def showAllTeam(request):
    teams = Team.objects.all()  # Récupère toutes les équipes
    return render(request, 'all_teams.html', {'teams': teams})

def showTeam(request, id):
    team = Team.objects.get(id=id)  # Récupère l'équipe spécifique par son ID
    pokemons = team.pokemons.all()  # Récupère tous les Pokémon dans cette équipe

    pokemons_details = []

    for pokemon in pokemons:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon.number}")
        if response.status_code == 200:
            pokemon_data = response.json()
            types = [t['type']['name'] for t in pokemon_data['types']]
            image_url = pokemon_data['sprites']['other']['official-artwork']['front_default']

            pokemons_details.append({
                'name': pokemon_data['name'],
                'image': image_url,
                'types': types
            })

    return render(request, 'team_detail.html', {'team': team, 'pokemons': pokemons_details})

def add_pokemon_to_team(request, pokedex_number):
    if request.method == 'POST':
        team_id = request.POST.get('teamId')
        team = get_object_or_404(Team, id=team_id)

        # Récupérer les détails du Pokémon depuis PokeAPI
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokedex_number}/')
        if response.status_code == 200:
            pokemon_data = response.json()

            # Créer ou récupérer l'instance du Pokémon
            pokemon, created = Pokemon.objects.get_or_create(
                number=pokedex_number,
                defaults={
                    'name': pokemon_data['name'],
                    # Ajoutez d'autres champs nécessaires ici
                }
            )

            # Récupérer les attaques et sélectionner aléatoirement 4 attaques
            all_attacks = [attack['move']['name'] for attack in pokemon_data['moves']]
            selected_attacks = random.sample(all_attacks, min(len(all_attacks), 4))

            # Ajouter les attaques sélectionnées au Pokémon
            for attack_name in selected_attacks:
                attack_response = requests.get(f'https://pokeapi.co/api/v2/move/{attack_name}/')
                if attack_response.status_code == 200:
                    attack_details = attack_response.json()
                    print(attack_details.get('accuracy'))
                    attack, _ = Attack.objects.get_or_create(
                        name=attack_name,
                        defaults={
                            'attack_type': attack_details['type']['name'],
                            'power': attack_details.get('accuracy'),
                            # Ajoutez ici les autres champs nécessaires
                        }
                    )
                    pokemon.attacks.add(attack)

            # Ajouter le Pokémon à l'équipe
            team.pokemons.add(pokemon)
            team.save()
        else:
            print("Erreur lors de la récupération des données du Pokémon")

        return redirect('team_detail', id=team_id)

    return redirect('index_pokedex')
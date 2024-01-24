from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse
from .models import Pokemon, Attack
from team.models import Team
from django.core.paginator import Paginator

# Recuperer 10 pokemon
def get_pokemons(page=1, limit=12):
    offset = (page - 1) * limit
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}')
    return response.json()

# Afficher les informations d'un pokémon
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

# Ajoutez un pokémon dans la team
'''
def add_pokemon_team(request, pokedex_number, user_id):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokedex_number}/')
    pokemon_details = response.json()
    pokemon, created = Pokemon.objects.get_or_create(
        number = pokedex_number,
        defaults={
            'name': pokemon_details['name'],
            'type1': pokemon_details['types'][0]['type']['name'],
            'type2': pokemon_details['types'][1]['type']['name'] if len(pokemon_details['types']) > 1 else None,
            'hp': pokemon_details['stats'][0]['base_stat'],
            'attack': pokemon_details['stats'][1]['base_stat'],
            'defense': pokemon_details['stats'][2]['base_stat'],
            'special_defense': pokemon_details['stats'][3]['base_stat'],
            'defense_sp': pokemon_details['stats'][4]['base_stat'],
            'speed': pokemon_details['stats'][5]['base_stat'],
        }
    )

    user = User.objects.get(id=user_id)
    team, created = Team.objects.get_or_create(user=user)

    team.pokemons.add(pokemon)
    team.save()
'''

def recherche_pokemon(search_query, page=1, limit=10):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon?limit=1000')  # Obtenez une grande liste de Pokémon
    all_pokemons = response.json()['results']

    # Filtrer les Pokémon par le nom de recherche
    filtered_pokemons = [pokemon for pokemon in all_pokemons if search_query.lower() in pokemon['name'].lower()]

    # Pagination
    paginator = Paginator(filtered_pokemons, limit)
    pokemons_page = paginator.get_page(page)

    return {
        'results': pokemons_page.object_list,
        'count': paginator.count
    }


# Create your views here. Affichez les pokemons
def index_pokedex(request):
    search_query = request.GET.get('search', '')
    page = int(request.GET.get('page', 1))
    if search_query:
        data = recherche_pokemon(search_query, page)
    else:
        data = get_pokemons(page)
    total_pokemon = data['count']
    total_pages = (total_pokemon + 9) // 10

    pokemons = []
    for pokemon in data['results']:
        detail_response = requests.get(pokemon['url'])
        detail_data = detail_response.json()

        sprites = detail_data.get('sprites', {})
        pokemons.append({
            'name': detail_data['name'],
            'image': sprites.get('front_default', 'default-image-url'),
            'pokedex_number': detail_data['id']
        })

    return render(request, 'pokedex/index.html', {
        'pokemons': pokemons,
        'current_page': page,
        'total_pages': total_pages,
        'total_pokemon': total_pokemon
    })

def detail_pokemon_view(request, pokedex_number):
    pokemon_details = get_pokemon_details(pokedex_number)
    total_team = Team.objects.count()
    teams = Team.objects.all()    
    return render(request, 'pokedex/detail_pokemon.html', {'pokemon': pokemon_details, 'teams': teams})


"""
def save_attack_view(request):
    if request.method == 'POST':
        # Ici, 'selected_attacks' est le nom du champ dans votre formulaire HTML.
        selected_attacks = request.POST.getlist('selected_attacks')
        if selected_attacks:
            # Limitez le nombre d'attaques à 4
            selected_attacks = selected_attacks[:4]
            Attack.saveAttack(selected_attacks)
            return redirect('success_view')  # Rediriger vers une vue de succès
        else:
            return HttpResponse("Aucune attaque sélectionnée", status=400)

    # Supposons que vous ayez une liste d'attaques à afficher à l'utilisateur
    all_attacks = ["thunderbolt", "surf", "flamethrower", "ice-beam"]  # Exemple de liste
    return render(request, 'save_attack.html', {'all_attacks': all_attacks})

# Vue pour montrer le succès de l'opération
def success_view(request):
    return render(request, 'success.html')
"""


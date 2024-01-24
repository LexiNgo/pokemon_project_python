import random
import json
from pokedex import Pokemon


with open('pokedex/type_tableur.json', 'r') as f:
    data = json.load(f)

def calculate_damage(attacker, defender):
    level = 50
    critical = 1  # assuming no critical hit
    A = attacker['stats'][1]['base_stat']
    D = defender['stats'][2]['base_stat']
    if A > 255 or D > 255:
        A //= 4
        D //= 4
    random_factor = random.randint(217, 255) / 255

    # Get type effectiveness from the matrix using the type index
    type_effectiveness_matrix = data['type_effectiveness_matrix']
    type_index = data['type_index']

    defender_types = [type_info['type']['name'] for type_info in defender['types']]

    # Calculate the type effectiveness
    move_type = attacker['types'][0]['type']['name']
    type1 = type_effectiveness_matrix[type_index[move_type]][type_index[defender_types[0]]]
    type2 = 1 if len(defender_types) == 1 else type_effectiveness_matrix[type_index[move_type]][type_index[defender_types[1]]]

    # Include type effectiveness in the damage calculation
    damage = ((((2 * level * critical / 5) + 2) * 100 * A / D) / 50 + 2) * type1 * type2 * random_factor
    print(damage)
    damage = max(0, damage)
    return int(damage)
from django.db import models
from pokedex.models import Pokemon, Attack

class Team(models.Model):
    name = models.CharField(max_length=30)
    pokemons = models.ManyToManyField(Pokemon)

    def __str__(self):
        return self.name

    @staticmethod
    def createTeam(name_team):
        team = Team(name=name_team)
        team.save()
        return team

    @staticmethod
    def deleteTeam(name_team):
        try:
            team = Team.objects.get(name=name_team)
            team.delete()
            return True
        except Team.DoesNotExist:
            return False

    @staticmethod
    def renameTeam(old_name, new_name):
        try:
            team = Team.objects.get(name=old_name)
            team.name = new_name
            team.save()
            return True
        except Team.DoesNotExist:
            return False

    def addPokemonTeam(self, pokemon, attack_names):
        # Vérifiez si l'équipe a moins de 6 Pokémon
        if self.pokemons.count() < 6:
            # Ajoutez le Pokémon à l'équipe
            self.pokemons.add(pokemon)

            # Enregistrez les attaques sélectionnées pour ce Pokémon
            for attack_name in attack_names:
                # Utilisez la fonction saveAttack pour enregistrer l'attaque
                # Assurez-vous que saveAttack est ajustée pour gérer une attaque à la fois
                Attack.saveAttack(attack_name)

                # Associez l'attaque au Pokémon
                attack = Attack.objects.get(name=attack_name)
                pokemon.attacks.add(attack)

            return True
        else:
            return False
        
    @staticmethod
    def clearAllPokemonTeam(name_team):
        try:
            team = Team.objects.get(name=name_team)
            team.pokemons.clear()
            return True
        except Team.DoesNotExist:
            return False

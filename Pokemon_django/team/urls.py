from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_team, name='create_team'),
    path('delete/<str:team_name>/', views.delete_team, name='delete_team'),
    path('rename/<str:old_name>/', views.rename_team, name='rename_team'),
    path('add_pokemon_to_team/<int:pokedex_number>/', views.add_pokemon_to_team, name='add_pokemon_to_team'),
    path('clear/<str:team_name>/', views.clear_pokemons_from_team, name='clear_pokemons_from_team'),
    path('all/', views.showAllTeam, name='show_all_teams'),
    path('<int:id>/', views.showTeam, name='team_detail'),
]

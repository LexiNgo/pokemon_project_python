from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_pokedex, name='index_pokedex'),
    path('<int:pokedex_number>/', views.detail_pokemon_view, name='detail_pokemon')
]
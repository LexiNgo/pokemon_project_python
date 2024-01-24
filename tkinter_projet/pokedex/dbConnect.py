import sqlite3

connexion = sqlite3.connect("pokedex/db.sqlite3")
curseur = connexion.cursor()
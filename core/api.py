from ninja import NinjaAPI
from livros.api import livros_router

api = NinjaAPI() #criação da instancia (variavel) do tipo ninjaapi
api.add_router('livros', livros_router)
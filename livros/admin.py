from django.contrib import admin
from .models import Livros, categorias

# Register your models here.
admin.site.register(categorias)
admin.site.register(Livros)

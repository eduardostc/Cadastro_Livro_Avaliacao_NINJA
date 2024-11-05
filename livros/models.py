from django.db import models

class categorias(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

# Create your models here.
class Livros(models.Model):
    streaming_choices = (('AK', 'Amazon Kindle'), ('F', 'Físico'))

    nome = models.CharField(max_length=50)
    streaming = models.CharField(max_length=2, choices=streaming_choices)
    nota = models.IntegerField(null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)
    categorias = models.ManyToManyField(categorias)

    def __str__(self):
        return self.nome  
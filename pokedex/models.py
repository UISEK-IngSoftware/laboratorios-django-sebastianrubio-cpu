from random import choices

from django.db import models

# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length=100, null=False)
    pokemon_type = {'Water','W'
            'Fire', 'F'
            'Grass', 'G'
            'Electric', 'E'
            'Psychic', 'P'
            'Ice', 'I'
            'Dragon', 'D'
            'Dark', 'DK'
            'Fairy', 'FA'}
    type = models.CharField(max_length=30,choices=pokemon_type, null=False)
    height = models.FloatField(null=False)
    weight = models.FloatField(null=False)
    
    
    def __str__(self):
        return self.name
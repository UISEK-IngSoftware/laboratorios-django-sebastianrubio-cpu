from random import choices

from django.db import models

class Trainer(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    birth_date = models.DateField(null=False)
    level = models.IntegerField(null=False)
    
    
    REGION_CHOICES = [
        ('K', 'Kanto'),
        ('J', 'Johto'),
        ('H', 'Hoenn'),
        ('S', 'Sinnoh'),
        ('U', 'Unova'),
        ('KA', 'Kalos'),
        ('A', 'Alola'),
        ('G', 'Galar'),
        ('P', 'Paldea'),
        ('NA', 'No Definida'),
    ]
    region = models.CharField(
        max_length=2, 
        choices=REGION_CHOICES, 
        default='NA'
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Pokemon(models.Model):
    name = models.CharField(max_length=100, null=False)
    
    POKEMON_TYPES = [
        ('W', 'Water'),
        ('F', 'Fire'),
        ('G', 'Grass'),
        ('E', 'Electric'),
        ('P', 'Psychic'),
        ('I', 'Ice'),
        ('D', 'Dragon'),
        ('DK', 'Dark'),
        ('FA', 'Fairy')
    ]
    
    type = models.CharField(max_length=30, choices=POKEMON_TYPES, null=False)
    height = models.FloatField(null=False)
    weight = models.FloatField(null=False)
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name
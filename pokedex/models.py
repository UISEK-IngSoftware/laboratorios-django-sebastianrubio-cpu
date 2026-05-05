from django.db import models

# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length=100, null=False)
    type = models.CharField(max_length=50, null=False)
    height = models.FloatField(null=False)
    weight = models.FloatField(null=False)
    
    def __str__(self):
        return self.name
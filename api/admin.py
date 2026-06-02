from django.contrib import admin
from .models import Pokemon, Trainer


# Register your models here.
admin.site.register(Pokemon)
class TrainerAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Trainer)
class PokemonAdmin(admin.ModelAdmin):
    pass

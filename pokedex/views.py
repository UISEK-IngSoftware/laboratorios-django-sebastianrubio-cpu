from django.http import HttpResponse
from django.template import loader
from .models import Pokemon, Trainer

def index(request):
    pokemons = Pokemon.objects.all()
    trainers = Trainer.objects.all()
    template = loader.get_template('index.html')
    
    context = {
        'pokemons': pokemons,
        'trainers': trainers
    }
    return HttpResponse(template.render(context, request))

def pokemon(request, id: int):
    pokemon = Pokemon.objects.get(id=id)
    template = loader.get_template('display_pokemon.html')
    context = {
        'pokemon': pokemon
    }
    return HttpResponse(template.render(context, request))

def trainer(request, id: int):
    trainer = Trainer.objects.get(id=id)
    # Necesitas crear este template 'display_trainer.html' en tu carpeta templates
    template = loader.get_template('display_trainer.html') 
    context = {
        'trainer': trainer
    }
    return HttpResponse(template.render(context, request))
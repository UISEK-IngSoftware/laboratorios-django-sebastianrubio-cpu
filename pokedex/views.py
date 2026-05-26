from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pokemon, Trainer
from django.contrib.auth.views import LoginView

# --- OPERACIONES PARA POKEMON ---

def edit_pokemon(request, id):
    pokemon = get_object_or_404(Pokemon, id=id)
    trainers = Trainer.objects.all()
    
    if request.method == 'POST':
        pokemon.name = request.POST.get('name')
        pokemon.type = request.POST.get('type')
        
        # Procesamiento estricto del archivo multimedia
        if 'picture' in request.FILES:
            pokemon.picture = request.FILES['picture']
            
        pokemon.save()
        return redirect('pokedex:index')
        
    return render(request, 'edit_pokemon.html', {'pokemon': pokemon, 'trainers': trainers})

def delete_pokemon(request, id):
    pokemon = get_object_or_404(Pokemon, id=id)
    pokemon.delete()
    return redirect('pokedex:index')


# --- OPERACIONES PARA TRAINER ---

def edit_trainer(request, id):
    trainer = get_object_or_404(Trainer, id=id)
    
    if request.method == 'POST':
        # Mapeo corregido a las columnas reales de la base de datos
        trainer.first_name = request.POST.get('first_name')
        trainer.last_name = request.POST.get('last_name')
        trainer.birth_date = request.POST.get('birth_date')
        trainer.level = request.POST.get('level')
        trainer.region = request.POST.get('region')
        
        # Procesamiento estricto del archivo multimedia
        if 'picture' in request.FILES:
            trainer.picture = request.FILES['picture']
            
        trainer.save()
        return redirect('pokedex:index')
        
    return render(request, 'edit_trainer.html', {'trainer': trainer})

def delete_trainer(request, id):
    trainer = get_object_or_404(Trainer, id=id)
    trainer.delete()
    return redirect('pokedex:index')


# --- VISTAS DE RENDERIZADO (INDEX Y DISPLAY) ---

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
    pokemon = get_object_or_404(Pokemon, id=id)
    template = loader.get_template('display_pokemon.html')
    context = {
        'pokemon': pokemon
    }
    return HttpResponse(template.render(context, request))

def trainer(request, id: int):
    trainer = get_object_or_404(Trainer, id=id)
    template = loader.get_template('display_trainer.html') 
    context = {
        'trainer': trainer
    }
    return HttpResponse(template.render(context, request))

class CustomLogInView(LoginView):
    template_name = 'login.html'
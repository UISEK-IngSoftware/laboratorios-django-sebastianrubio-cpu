from django.http import HttpResponse
from django.template import loader
from .models import Pokemon, Trainer
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Pokemon, Trainer


def edit_pokemon(request, id):
    pokemon = get_object_or_404(Pokemon, id=id)
    trainers = Trainer.objects.all() # Necesario si el modelo tiene llave foránea a Trainer
    
    if request.method == 'POST':
        pokemon.name = request.POST.get('name')
        pokemon.type = request.POST.get('type')
        
        # Procesar nueva imagen solo si se cargó un archivo
        if 'picture' in request.FILES:
            pokemon.picture = request.FILES['picture']
            
        pokemon.save()
        return redirect('index')
        
    return render(request, 'edit_pokemon.html', {'pokemon': pokemon, 'trainers': trainers})

def delete_pokemon(request, id):
    pokemon = get_object_or_404(Pokemon, id=id)
    pokemon.delete()
    return redirect('index')


# --- OPERACIONES PARA TRAINER ---

def edit_trainer(request, id):
    trainer = get_object_or_404(Trainer, id=id)
    
    if request.method == 'POST':
        # Mapeo explícito a las nuevas columnas del modelo
        trainer.first_name = request.POST.get('first_name')
        trainer.last_name = request.POST.get('last_name')
        trainer.birth_date = request.POST.get('birth_date')
        trainer.level = request.POST.get('level')
        trainer.region = request.POST.get('region')
        
        # Procesamiento del archivo físico de imagen
        if 'picture' in request.FILES:
            trainer.picture = request.FILES['picture']
            
        trainer.save()
        return redirect('index')
        
    return render(request, 'edit_trainer.html', {'trainer': trainer})
def delete_trainer(request, id):
    trainer = get_object_or_404(Trainer, id=id)
    trainer.delete()
    return redirect('index')


def index(request):
    pokemons = Pokemon.objects.all()
    trainers = Trainer.objects.all()
    template = loader.get_template('index.html')
    
    context = {
        'pokemons': pokemons,
        'trainers': trainers,
        'MEDIA_URL': settings.MEDIA_URL
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
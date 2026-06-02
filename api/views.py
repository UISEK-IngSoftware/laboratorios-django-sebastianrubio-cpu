from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pokemon, Trainer
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages


# --- OPERACIONES PARA POKEMON ---

@login_required
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
@login_required
def delete_pokemon(request, id):
    pokemon = get_object_or_404(Pokemon, id=id)
    pokemon.delete()
    return redirect('pokedex:index')


# --- OPERACIONES PARA TRAINER ---

@login_required 
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
@login_required
def delete_trainer(request, id):
    trainer = get_object_or_404(Trainer, id=id)
    trainer.delete()
    return redirect('pokedex:index')


# --- VISTAS DE RENDERIZADO (INDEX Y DISPLAY) ---

@login_required
def index(request):
    pokemons = Pokemon.objects.all()
    trainers = Trainer.objects.all()
    template = loader.get_template('index.html')
    
    context = {
        'pokemons': pokemons,
        'trainers': trainers
    }
    return HttpResponse(template.render(context, request))

@login_required 
def pokemon(request, id: int):
    pokemon = get_object_or_404(Pokemon, id=id)
    template = loader.get_template('display_pokemon.html')
    context = {
        'pokemon': pokemon
    }
    return HttpResponse(template.render(context, request))
@login_required
def trainer(request, id: int):
    trainer = get_object_or_404(Trainer, id=id)
    template = loader.get_template('display_trainer.html') 
    context = {
        'trainer': trainer
    }
    return HttpResponse(template.render(context, request))


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inyectar clases de Bootstrap a los campos
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        
class CustomLogInView(LoginView):
    template_name = 'login_form.html' # Asegúrate de que coincida con tu archivo
    authentication_form = CustomLoginForm # <--- IMPORTANTE: Conectar el form
    
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('pokedex:login')

    def form_valid(self, form):
        messages.success(self.request, "¡Cuenta creada exitosamente! Ya puedes iniciar sesión.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al crear la cuenta. Por favor, verifica los datos.")
        return super().form_invalid(form)
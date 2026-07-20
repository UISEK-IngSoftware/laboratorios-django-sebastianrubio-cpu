import requests
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from .serializer import PokemonSerializer, TrainerSerializer
from pokedex.models import Pokemon, Trainer


class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer

# AUTENTICACIÓN GITHUB

class GitHubLoginAPIView(APIView):
    # Endpoint público, el usuario aún no tiene JWT local
    permission_classes = []

    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        
        if not code:
            return Response(
                {"error": "El código de autorización de GitHub es obligatorio."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        client_id = 'Ov23likwZH3eFzuhDbEn'
        client_secret = 'd65ffe418abd7b1d24a2d735f30c1bd0fab7c2bf'

        # 1. Intercambio del código temporal por el access_token de GitHub
        token_response = requests.post(
            'https://github.com/login/oauth/access_token',
            data={
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code,
            },
            headers={'Accept': 'application/json'}
        )
        
        access_token = token_response.json().get('access_token')
        
        if not access_token:
            return Response(
                {"error": "GitHub rechazó el código o expiró."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 2. Consumo de la API de GitHub para obtener la identidad del usuario
        user_response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if user_response.status_code != 200:
            return Response({"error": "Error de permisos al leer perfil."}, status=status.HTTP_401_UNAUTHORIZED)
            
        user_data = user_response.json()
        username = user_data.get('login')
        email = user_data.get('email')

        # Si el correo está oculto, forzamos su obtención
        if not email:
            email_response = requests.get(
                'https://api.github.com/user/emails',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            if email_response.status_code == 200:
                emails = email_response.json()
                email = next((e['email'] for e in emails if e['primary']), None)
        
        if not email:
            email = f"{username}@github-placeholder.com"

        # 3. Consolidación del usuario local en SQLite
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': user_data.get('name', username)[:30]
            }
        )
        
        # 4. Emisión de JWT local
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "username": user.username,
                "email": user.email
            }
        }, status=status.HTTP_200_OK)
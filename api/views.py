from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
import requests
from django.contrib.auth.models import User
from .serializer import PokemonSerializer, TrainerSerializer
from pokedex.models import Pokemon, Trainer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or request.user.groups.filter(name='Admin').exists()
        )

class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    permission_classes = [IsAdminOrReadOnly]

class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    permission_classes = [IsAdminOrReadOnly]

class GitHubLoginAPIView(APIView):
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

        user_response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if user_response.status_code != 200:
            return Response({"error": "Error de permisos al leer perfil."}, status=status.HTTP_401_UNAUTHORIZED)
            
        user_data = user_response.json()
        username = user_data.get('login')
        email = user_data.get('email')

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

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': user_data.get('name', username)[:30]
            }
        )
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_staff or user.groups.filter(name='Admin').exists()
            }
        }, status=status.HTTP_200_OK)
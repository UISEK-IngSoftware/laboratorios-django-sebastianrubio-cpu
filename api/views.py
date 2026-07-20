from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializer import PokemonSerializer, TrainerSerializer
from pokedex.models import Pokemon, Trainer
from django.contrib.auth import authenticate
from oauth2_provider.models import Application


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


class OAuth2TokenAPIView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        grant_type = request.data.get('grant_type')
        client_id = request.data.get('client_id')

        if grant_type != 'password':
            return Response({"error": "unsupported_grant_type"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            app = Application.objects.get(client_id=client_id, client_type='public')
        except Application.DoesNotExist:
            return Response({"error": "invalid_client"}, status=status.HTTP_401_UNAUTHORIZED)

        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "invalid_request"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "invalid_grant"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "token_type": "Bearer",
            "expires_in": 3600
        }, status=status.HTTP_200_OK)   
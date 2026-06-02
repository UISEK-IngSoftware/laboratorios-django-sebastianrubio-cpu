from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), # Esta línea es crítica
    # Posiblemente también tengas: path('', include('pokedex.urls')),
]
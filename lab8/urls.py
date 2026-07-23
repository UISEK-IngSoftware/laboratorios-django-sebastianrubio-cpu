from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from pokedex.auth_view import CustomTokenView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pokedex.urls')),
    path('api/', include('api.urls')),
    path('api/oauth/token/', CustomTokenView.as_view(), name='token'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
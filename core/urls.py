from django.urls import path, include
from django.contrib import admin
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('/unidades/home')),
    path('usuarios/', include('usuarios.urls')),
    path('unidades/', include('unidades.urls')),
]
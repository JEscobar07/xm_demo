from django.contrib import admin
from django.urls import path
from simulatorXn import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('registrar/', views.registrar_frontera, name='registrar_frontera'),
]

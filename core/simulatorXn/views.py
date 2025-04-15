from django.shortcuts import render, redirect
from .forms import FronteraForm
import os
from dotenv import load_dotenv

load_dotenv()
env_user = os.getenv("FORM_USERNAME")
env_pass = os.getenv("FORM_PASSWORD")

def login_view(request):
    """
    Simulates a basic login using hardcoded credentials.
    Sets session variable if successful.
    """

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == env_user and password == env_pass:
            request.session['usuario'] = username
            return redirect('registrar_frontera')
        return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    # GET
    return render(request, 'login.html')


def registrar_frontera(request):
    """
    Handles the form submission for creating a new Frontera record.
    Requires user to be logged in via session.
    """
    if not request.session.get('usuario'):
        return redirect('login')

    form = FronteraForm()
    if request.method == 'POST':
        form = FronteraForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()

            request.session['frontera_data'] = {
                'requerimiento': instance.requerimiento,
                'frontera': instance.frontera,
                'usuario': instance.usuario,
                'equipo_medida': instance.equipo_medida,
                'curva_tipica': instance.curva_tipica,
                'certificaciones': instance.certificaciones,
                'adjunto': instance.adjunto.name if instance.adjunto else ''
            }

            return render(request, 'registrado.html')

    return render(request, 'registro.html', {'form': form})

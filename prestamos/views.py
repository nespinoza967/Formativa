from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .permisos import encargado_required


@login_required
def inicio(request):
    return render(request, 'prestamos/inicio.html')


@encargado_required
def panel_encargado(request):
    return render(request, 'prestamos/panel_encargado.html')

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoriaForm, HerramientaForm
from .models import Categoria, Herramienta
from .permisos import encargado_required


@login_required
def inicio(request):
    return render(request, 'prestamos/inicio.html')


@encargado_required
def panel_encargado(request):
    return render(request, 'prestamos/panel_encargado.html')


# ---------- Herramientas (solo encargado) ----------

@encargado_required
def herramienta_list(request):
    herramientas = Herramienta.objects.select_related('categoria')
    q = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '')
    if q:
        herramientas = herramientas.filter(nombre__icontains=q)
    if categoria_id.isdigit():
        herramientas = herramientas.filter(categoria_id=categoria_id)
    return render(request, 'prestamos/herramienta_list.html', {
        'herramientas': herramientas,
        'categorias': Categoria.objects.all(),
        'q': q,
        'categoria_id': categoria_id,
    })


@encargado_required
def herramienta_detail(request, pk):
    herramienta = get_object_or_404(Herramienta.objects.select_related('categoria'), pk=pk)
    return render(request, 'prestamos/herramienta_detail.html', {'herramienta': herramienta})


@encargado_required
def herramienta_create(request):
    form = HerramientaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            herramienta = form.save()
            messages.success(request, f'Herramienta "{herramienta}" creada correctamente.')
            return redirect('herramienta_list')
        messages.error(request, 'Revisa los errores del formulario.')
    return render(request, 'prestamos/herramienta_form.html', {'form': form, 'titulo': 'Nueva herramienta'})


@encargado_required
def herramienta_update(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    form = HerramientaForm(request.POST or None, instance=herramienta)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f'Herramienta "{herramienta}" actualizada correctamente.')
            return redirect('herramienta_list')
        messages.error(request, 'Revisa los errores del formulario.')
    return render(request, 'prestamos/herramienta_form.html', {'form': form, 'titulo': 'Editar herramienta'})


@encargado_required
def herramienta_delete(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    if request.method == 'POST':
        try:
            herramienta.delete()
            messages.success(request, f'Herramienta "{herramienta}" eliminada.')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar: la herramienta tiene préstamos registrados.')
        return redirect('herramienta_list')
    return render(request, 'prestamos/confirmar_eliminar.html', {
        'objeto': herramienta, 'tipo': 'la herramienta', 'cancelar_url': 'herramienta_list',
    })


# ---------- Categorías (solo encargado) ----------

@encargado_required
def categoria_list(request):
    return render(request, 'prestamos/categoria_list.html', {'categorias': Categoria.objects.all()})


@encargado_required
def categoria_create(request):
    form = CategoriaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria}" creada correctamente.')
            return redirect('categoria_list')
        messages.error(request, 'Revisa los errores del formulario.')
    return render(request, 'prestamos/categoria_form.html', {'form': form, 'titulo': 'Nueva categoría'})


@encargado_required
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f'Categoría "{categoria}" actualizada correctamente.')
            return redirect('categoria_list')
        messages.error(request, 'Revisa los errores del formulario.')
    return render(request, 'prestamos/categoria_form.html', {'form': form, 'titulo': 'Editar categoría'})


@encargado_required
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        try:
            categoria.delete()
            messages.success(request, f'Categoría "{categoria}" eliminada.')
        except ProtectedError:
            messages.error(request, f'No se puede eliminar "{categoria}": tiene herramientas asociadas.')
        return redirect('categoria_list')
    return render(request, 'prestamos/confirmar_eliminar.html', {
        'objeto': categoria, 'tipo': 'la categoría', 'cancelar_url': 'categoria_list',
    })

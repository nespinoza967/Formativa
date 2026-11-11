from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import CategoriaForm, HerramientaForm
from .models import Categoria, Herramienta, Prestamo
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


# ---------- Solicitud de préstamo (carrito en la sesión) ----------

MAX_SOLICITUD = 3
DIAS_PRESTAMO = 7


def herramientas_prestables():
    """Herramientas que un socio puede pedir: disponibles y que no estén en reparación."""
    return (Herramienta.objects.select_related('categoria')
            .filter(disponible=True)
            .exclude(estado=Herramienta.ESTADO_REPARACION))


@login_required
def catalogo(request):
    return render(request, 'prestamos/catalogo.html', {
        'herramientas': herramientas_prestables(),
        'solicitud': request.session.get('solicitud', []),
        'max_solicitud': MAX_SOLICITUD,
    })


@login_required
@require_POST
def agregar_solicitud(request, id):
    herramienta = get_object_or_404(herramientas_prestables(), pk=id)
    solicitud = request.session.get('solicitud', [])

    if herramienta.id in solicitud:
        messages.warning(request, f'"{herramienta.nombre}" ya está en tu solicitud.')
    elif len(solicitud) >= MAX_SOLICITUD:
        messages.error(request, f'Tu solicitud no puede tener más de {MAX_SOLICITUD} herramientas.')
    else:
        solicitud.append(herramienta.id)
        request.session['solicitud'] = solicitud
        messages.success(request, f'"{herramienta.nombre}" agregada a tu solicitud.')
    return redirect('catalogo')


@login_required
def ver_solicitud(request):
    ids = request.session.get('solicitud', [])
    herramientas = Herramienta.objects.select_related('categoria').filter(id__in=ids)
    return render(request, 'prestamos/solicitud.html', {'herramientas': herramientas})


@login_required
@require_POST
def quitar_solicitud(request, id):
    solicitud = request.session.get('solicitud', [])
    if id in solicitud:
        solicitud.remove(id)
        request.session.modified = True
        messages.success(request, 'Herramienta quitada de tu solicitud.')
    else:
        messages.warning(request, 'Esa herramienta no estaba en tu solicitud.')
    return redirect('ver_solicitud')


@login_required
@require_POST
def confirmar_solicitud(request):
    ids = request.session.get('solicitud', [])
    if not ids:
        messages.warning(request, 'Tu solicitud está vacía.')
        return redirect('catalogo')

    hoy = timezone.localdate()
    creados, no_disponibles = [], []
    with transaction.atomic():
        # select_for_update bloquea las filas para que dos socios no pidan la misma herramienta a la vez
        for herramienta in Herramienta.objects.select_for_update().filter(id__in=ids):
            if not herramienta.disponible or herramienta.estado == Herramienta.ESTADO_REPARACION:
                no_disponibles.append(herramienta.nombre)
                continue
            Prestamo.objects.create(
                socio=request.user,
                herramienta=herramienta,
                fecha_solicitud=hoy,
                fecha_devolucion_esperada=hoy + timedelta(days=DIAS_PRESTAMO),
                estado=Prestamo.ESTADO_PENDIENTE,
            )
            herramienta.disponible = False
            herramienta.save(update_fields=['disponible'])
            creados.append(herramienta.nombre)

    del request.session['solicitud']

    if creados:
        messages.success(request, f'Solicitud enviada: {len(creados)} préstamo(s) pendiente(s) ({", ".join(creados)}).')
    if no_disponibles:
        messages.error(request, f'Ya no estaban disponibles: {", ".join(no_disponibles)}.')
    return redirect('mis_prestamos')


@login_required
def mis_prestamos(request):
    prestamos = Prestamo.objects.select_related('herramienta').filter(socio=request.user)
    return render(request, 'prestamos/mis_prestamos.html', {'prestamos': prestamos})

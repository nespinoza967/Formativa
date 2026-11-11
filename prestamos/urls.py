from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('encargado/', views.panel_encargado, name='panel_encargado'),

    # Herramientas
    path('herramientas/', views.herramienta_list, name='herramienta_list'),
    path('herramientas/nueva/', views.herramienta_create, name='herramienta_create'),
    path('herramientas/<int:pk>/', views.herramienta_detail, name='herramienta_detail'),
    path('herramientas/<int:pk>/editar/', views.herramienta_update, name='herramienta_update'),
    path('herramientas/<int:pk>/eliminar/', views.herramienta_delete, name='herramienta_delete'),

    # Categorías
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/nueva/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', views.categoria_delete, name='categoria_delete'),

    # Solicitud de préstamo (sesión)
    path('catalogo/', views.catalogo, name='catalogo'),
    path('solicitud/', views.ver_solicitud, name='ver_solicitud'),
    path('solicitud/agregar/<int:id>/', views.agregar_solicitud, name='agregar_solicitud'),
    path('solicitud/quitar/<int:id>/', views.quitar_solicitud, name='quitar_solicitud'),
    path('solicitud/confirmar/', views.confirmar_solicitud, name='confirmar_solicitud'),

    # Préstamos
    path('mis-prestamos/', views.mis_prestamos, name='mis_prestamos'),
    path('mis-prestamos/<int:pk>/cancelar/', views.cancelar_prestamo, name='cancelar_prestamo'),
    path('prestamos/', views.prestamo_list, name='prestamo_list'),
    path('prestamos/<int:pk>/activar/', views.activar_prestamo, name='activar_prestamo'),
    path('prestamos/<int:pk>/devolver/', views.registrar_devolucion, name='registrar_devolucion'),
]

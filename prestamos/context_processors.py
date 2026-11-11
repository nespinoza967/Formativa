def solicitud(request):
    """Deja disponible en todos los templates cuántas herramientas tiene la solicitud."""
    return {'solicitud_count': len(request.session.get('solicitud', []))}

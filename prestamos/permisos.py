"""Restricción de vistas solo para el encargado (usuario con is_staff)."""
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def es_encargado(user):
    return user.is_authenticated and user.is_staff


def encargado_required(vista):
    """Decorador para vistas basadas en funciones: exige sesión y is_staff."""
    return login_required(user_passes_test(es_encargado)(vista))


class EncargadoRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin para vistas basadas en clases: exige sesión y is_staff."""

    def test_func(self):
        return es_encargado(self.request.user)

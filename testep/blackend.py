from django.contrib.auth.backends import BaseBackend
from .models import Usuario

class UsuarioBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            usuario = Usuario.objects.get(emailusuario=email)
            if usuario.senhausuario == password:  # Comparar a senha simples é inseguro, use hashing
                return usuario
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
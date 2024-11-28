from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed

class CustomIsAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            raise AuthenticationFailed('Oldin ro‘yxatdan o‘ting.')
        return True



from rest_framework import permissions


class IsAuthenticatedOrOnlyCreate(permissions.BasePermission):
    # message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        """
        Permiso personalizado que permite a cualquier usuario realizar un POST (crear),
        pero requiere autenticación para otros métodos.
        """

        if request.method == "POST":
            return True
        return request.user and request.user.is_authenticated

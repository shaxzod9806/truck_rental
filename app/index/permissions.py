from rest_framework import permissions


class IsRenter(permissions.BasePermission):
    """
    Global permission check for Is user Renter
    """
    message = 'You are not Renter'

    def has_permission(self, request, view):
        user_type = request.user.user_type
        if int(user_type) == 3:
            return True
        else:
            return False


class IsCustomer(permissions.BasePermission):
    """
    Global permission check for Is user Customer
    """
    message = 'You are not Customer'

    def has_permission(self, request, view):
        user_type = request.user.user_type
        if int(user_type) == 4:
            return True
        else:
            return False


class IsManager(permissions.BasePermission):
    """
    Global permission check for Is user Manager`
    """
    message = 'You are not Customer'

    def has_permission(self, request, view):
        user_type = request.user.user_type
        if int(user_type) == 2:
            return True
        else:
            return False

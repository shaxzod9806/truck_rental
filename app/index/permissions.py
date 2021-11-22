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

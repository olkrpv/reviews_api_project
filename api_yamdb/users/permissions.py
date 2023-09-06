from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdminOrReadOnly(BasePermission):
    '''Доступ администратора или суперпользователя,
       для остальных - только для чтения.'''
    # def has_permission(self, request, view):
    #     return (
    #         request.method in SAFE_METHODS
    #         or request.user.is_authenticated
    #         or request.user.is_admin
    #     )
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAdmin(BasePermission):
    '''Доступ администратора или суперпользователя.'''

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )

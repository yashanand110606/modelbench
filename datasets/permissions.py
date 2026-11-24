from rest_framework.permissions import BasePermission

class HasDatasetScope(BasePermission):
    def has_permission(self, request, view):
        return request.oauth2_token.scope.contains('dataset')
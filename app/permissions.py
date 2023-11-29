from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsOwnerProduct(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.company == request.user

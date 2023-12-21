from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . import serializers
from apps.permissions import IsOwner


def home(request):
    return render(request, 'index.html')


class UserViewSets(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    http_method_names = ['get', 'POST', 'PUT', 'PATCH', 'DELETE']
    permission_classes = [IsOwner, IsAuthenticated]

    def list(self, request, *args, **kwargs):
        obj = get_object_or_404(User, id=request.user.id)
        serializers = self.get_serializer(
            instance=obj
        )
        return Response(serializers.data)

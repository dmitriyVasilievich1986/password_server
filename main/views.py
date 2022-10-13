from rest_framework.viewsets import GenericViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializer import PasswordsSerializer
from rest_framework import status, mixins
from .models import Passwords
from .secret_key import Key


class PasswordViewSet(GenericViewSet, mixins.DestroyModelMixin):
    serializer_class = PasswordsSerializer
    queryset = Passwords.objects.all()

    def list(self, request, *args, **kwargs) -> Response:
        queryset = Passwords.objects.all()
        serializer = PasswordsSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        key = Key(password=request.data["key"])
        password = key.encrypt(request.data["password"])
        p = Passwords(
            description=request.data.get("description"),
            name=request.data.get("name"),
            password=password,
        )
        p.save()
        return Response(p.json(), status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"])
    def get(self, request, *args, **kwargs) -> Response:
        key = Key(password=request.data["key"])
        if "id" in request.data:
            p = get_object_or_404(Passwords, id=request.data["id"])
        else:
            p = Passwords.objects.filter(name__icontains=request.data["name"])[0]
        data = p.json()
        data["password"] = key.decrypt(data["password"])
        return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        if "password" in request.data and "key" in request.data:
            key = Key(password=request.data["key"])
            instance.password = key.encrypt(request.data["password"])
        instance.description = request.data.get("description", instance.description)
        instance.name = request.data.get("name", instance.name)
        instance.save()
        return Response(instance.json(), status=status.HTTP_202_ACCEPTED)
